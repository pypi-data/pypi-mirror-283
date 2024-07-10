# ------------------------------------------------------ Imports ----------------------------------------------------- #
import os
import subprocess
import SimpleITK
import pydicom
import contextlib
import io
import dicom2nifti
import six
import re
import unicodedata

from ocelotz import system
from ocelotz import image_processing
from ocelotz import file_management


def remove_accents(filename):
    filename = filename.replace(" ", "_")
    if isinstance(filename, type(six.u(''))):
        unicode_filename = filename
    else:
        unicode_filename = six.u(filename)
    cleaned_filename = unicodedata.normalize('NFKD', unicode_filename).encode('ASCII', 'ignore').decode('ASCII')

    cleaned_filename = re.sub('[^\w\s-]', '', cleaned_filename.strip().lower())
    cleaned_filename = re.sub('[-\s]+', '-', cleaned_filename)

    return cleaned_filename


def predict_nifti_file_stem(input_dicom_directory: str):
    dicom_files = os.listdir(input_dicom_directory)
    reference_dicom_file = pydicom.read_file(os.path.join(input_dicom_directory, dicom_files[0]))

    base_filename = ""
    if 'SeriesNumber' in reference_dicom_file:
        base_filename = remove_accents('%s' % reference_dicom_file.SeriesNumber)
        if 'SeriesDescription' in reference_dicom_file:
            base_filename = remove_accents('%s_%s' % (base_filename, reference_dicom_file.SeriesDescription))
        elif 'SequenceName' in reference_dicom_file:
            base_filename = remove_accents('%s_%s' % (base_filename, reference_dicom_file.SequenceName))
        elif 'ProtocolName' in reference_dicom_file:
            base_filename = remove_accents('%s_%s' % (base_filename, reference_dicom_file.ProtocolName))
    else:
        base_filename = remove_accents(reference_dicom_file.SeriesInstanceUID)

    return base_filename


def to_nifti_2(input_dicom_directory: str, output_nifti_directory: str, output_nifti_filename: str):
    nifti_compression = False
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        dicom2nifti.convert_directory(input_dicom_directory, output_nifti_directory, compression=nifti_compression, reorient=True)

    predicted_nifti_file_stem = predict_nifti_file_stem(input_dicom_directory)
    if nifti_compression:
        predicted_nifti_filename = f"{predicted_nifti_file_stem}.nii.gz"
        output_nifti_filename = f"{output_nifti_filename}.nii.gz"
    else:
        predicted_nifti_filename = f"{predicted_nifti_file_stem}.nii"
        output_nifti_filename = f"{output_nifti_filename}.nii"
    predicted_file_path = os.path.join(output_nifti_directory, predicted_nifti_filename)
    output_nifti_file_path = os.path.join(output_nifti_directory, output_nifti_filename)
    os.rename(predicted_file_path, output_nifti_file_path)


def dcm2niix(input_dicom_directory: str, output_nifti_directory: str, output_nifti_filename: str):
    cmd_to_run: list[str] = [system.DCM2NIIX_PATH,
                             '-z', 'y',
                             '-o', output_nifti_directory,
                             '-f', output_nifti_filename,
                             input_dicom_directory]

    try:
        subprocess.run(cmd_to_run, capture_output=True, check=True)
        os.remove(os.path.join(output_nifti_directory, f'{output_nifti_filename}.json'))
        generated_nifti_files = file_management.get_NIFTI_files(output_nifti_directory)
        for generated_nifti_file in generated_nifti_files:
            if 'ROI' in generated_nifti_files:
                os.remove(os.path.join(output_nifti_directory, generated_nifti_file))
    except subprocess.CalledProcessError:
        to_nifti_2(input_dicom_directory, output_nifti_directory, output_nifti_filename)
        print(f"Error during DICOM to NIFTI conversion using dcm2niix. Using fallback.")


def dicom_to_nifti(dicom_directory: str, nifti_file_path: str):
    nifti_directory, nifti_file_name = os.path.split(nifti_file_path)
    nifti_file_stem = nifti_file_name.split(".", 1)[0]

    dcm2niix(dicom_directory, nifti_directory, nifti_file_stem)


# SUV computation is based on the guidelines of the Quantitative Imaging Biomarkers Alliance, mainly taken from:
# - https://qibawiki.rsna.org/index.php/Standardized_Uptake_Value_(SUV)
# - https://qibawiki.rsna.org/images/6/62/SUV_vendorneutral_pseudocode_happypathonly_20180626_DAC.pdf
def get_DICOM_PET_parameters(dicom_file_path: str) -> dict:
    """
    Get DICOM parameters from DICOM tags using pydicom
    :param dicom_file_path: Path to the DICOM file to get the SUV parameters from
    :return: DICOM_parameters, a dictionary with DICOM parameters
    """
    ds = pydicom.dcmread(dicom_file_path, stop_before_pixels=True)
    DICOM_parameters = {'PatientWeight': tag_to_float(ds.get('PatientWeight', None)),
                        'AcquisitionDate': ds.get('AcquisitionDate', None),
                        'AcquisitionTime': ds.get('AcquisitionTime', None),
                        'SeriesTime': ds.get('SeriesTime', None),
                        'DecayFactor': tag_to_float(ds.get('DecayFactor', None)),
                        'DecayCorrection': ds.get('DecayCorrection', None),
                        'RadionuclideTotalDose': None,
                        'RadiopharmaceuticalStartTime': None,
                        'RadionuclideHalfLife': None}

    if 'RadiopharmaceuticalInformationSequence' in ds:
        radiopharmaceutical_information = ds.RadiopharmaceuticalInformationSequence[0]
        DICOM_parameters['RadionuclideTotalDose'] = tag_to_float(radiopharmaceutical_information.get('RadionuclideTotalDose', None))
        DICOM_parameters['RadiopharmaceuticalStartTime'] = radiopharmaceutical_information.get('RadiopharmaceuticalStartTime', None)
        DICOM_parameters['RadionuclideHalfLife'] = tag_to_float(radiopharmaceutical_information.get('RadionuclideHalfLife', None))
    return DICOM_parameters


def tag_to_float(tag: str) -> float | None:
    if tag is None:
        return None
    return float(tag)


def tag_to_time_seconds(tag: str) -> int | None:
    if tag is None:
        return None
    time = tag.split('.')[0]
    hours, minutes, seconds = int(time[0:2]), int(time[2:4]), int(time[4:6])
    time_seconds = hours * 3600 + minutes * 60 + seconds
    return time_seconds


def get_time_difference_seconds(time_1: str, time_2: str) -> int | None:
    time_1_seconds = tag_to_time_seconds(time_1)
    time_2_seconds = tag_to_time_seconds(time_2)
    if time_1_seconds is None or time_2_seconds is None:
        return None

    time_difference_seconds = time_1_seconds - time_2_seconds
    return time_difference_seconds


def compute_corrected_activity(patient_parameters: dict) -> float | None:
    radiopharmaceutical_start_time = patient_parameters['RadiopharmaceuticalStartTime']
    series_time = patient_parameters['SeriesTime']
    injection_to_scan_time = get_time_difference_seconds(series_time, radiopharmaceutical_start_time)
    radionuclide_total_dose = patient_parameters['RadionuclideTotalDose']
    radionuclide_half_life = patient_parameters['RadionuclideHalfLife']

    if injection_to_scan_time is None or radionuclide_half_life is None:
        if radionuclide_total_dose is None:
            print("Important Information: Decay correction was not possible.")
            return None
        else:
            print("Important Information: Decay correction was not possible for existing dose.")
            return radionuclide_total_dose

    decay_corrected_activity = radionuclide_total_dose * pow(2.0, -(injection_to_scan_time / radionuclide_half_life))
    print(f"Original activity of {radionuclide_total_dose} MBq after {injection_to_scan_time/60} min is {decay_corrected_activity} MBq.")
    return decay_corrected_activity


def convert_bq_to_suv(bq_PET_file_path: str, patient_parameters: dict, suv_PET_file_path: str = None) -> SimpleITK.Image | None:
    """
    Convert a becquerel PET image to SUV image
    :param bq_PET_file_path: Path to a becquerel PET image to convert to SUV image (can be NRRD, NIFTI, ANALYZE
    :param suv_PET_file_path: Name of the SUV image to be created (preferably with a path)
    :param patient_parameters: A dictionary with the SUV parameters (weight in kg, dose in mBq)
    """

    patient_weight = patient_parameters["PatientWeight"]
    corrected_activity = compute_corrected_activity(patient_parameters)

    if patient_weight is None or corrected_activity is None:
        print("Important Information: SUV computation was not possible.")
        return None

    suv_conversion_factor = (patient_weight * 1000) / corrected_activity
    bq_image = SimpleITK.ReadImage(bq_PET_file_path, SimpleITK.sitkFloat32)
    suv_image = image_processing.scale_image(bq_image, suv_conversion_factor)

    if suv_PET_file_path is not None:
        SimpleITK.WriteImage(suv_image, suv_PET_file_path)

    return suv_image


def bq_PET_to_suv_PET(bq_PET_file_path: str, suv_PET_file_path: str, DICOM_PET_directory: str):
    DICOM_PET_files = file_management.get_DICOM_files(DICOM_PET_directory)
    DICOM_PET_file_probe = os.path.join(DICOM_PET_directory, DICOM_PET_files[0])
    DICOM_PET_parameters = get_DICOM_PET_parameters(DICOM_PET_file_probe)
    convert_bq_to_suv(bq_PET_file_path, DICOM_PET_parameters, suv_PET_file_path)
