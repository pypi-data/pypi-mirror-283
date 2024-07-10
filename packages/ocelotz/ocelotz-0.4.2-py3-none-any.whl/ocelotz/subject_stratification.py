# ------------------------------------------------------ Imports ----------------------------------------------------- #
import pydicom
import os

from ocelotz import file_management
from ocelotz import image_conversion


class Subject:
    def __init__(self, dicom_directory):
        self.DICOM_files = [os.path.join(dicom_directory, dicom_file) for dicom_file in os.listdir(dicom_directory)]
        self.BMI = self.determine_BMI()
        self.age = self.determine_age()
        self.sex = self.determine_sex()
        self.height = self.determine_height()

    def determine_BMI(self) -> float | None:
        BMI = None
        dicom_file = pydicom.read_file(self.DICOM_files[0])
        if "PatientSize" in dicom_file and "PatientWeight" in dicom_file:
            size = dicom_file.PatientSize
            weight = dicom_file.PatientWeight
            BMI = weight / size ** 2
        return BMI

    def determine_age(self) -> int | None:
        age = None
        dicom_file = pydicom.read_file(self.DICOM_files[0])
        if "PatientAge" in dicom_file:
            if isinstance(dicom_file.PatientAge, str) and dicom_file.PatientAge == "":
                return age
            age = int(''.join(digit for digit in dicom_file.PatientAge if digit.isdigit()))
        return age

    def determine_sex(self) -> str | None:
        sex = None
        dicom_file = pydicom.read_file(self.DICOM_files[0])
        if "PatientSex" in dicom_file:
            sex = dicom_file.PatientSex
        return sex

    def determine_height(self) -> float | None:
        size = None
        dicom_file = pydicom.read_file(self.DICOM_files[0])
        if "PatientSize" in dicom_file:
            size = dicom_file.PatientSize
        return size


def classify_sex(patient_sex: str) -> str:
    classified_sex = "undefined_sex"
    if patient_sex is None:
        return classified_sex
    if patient_sex == 'M':
        classified_sex = "male"
    elif patient_sex == 'F':
        classified_sex = "female"
    elif patient_sex == 'O':
        classified_sex = "other"
    return classified_sex


def classify_age(patient_age: int) -> str:
    classified_age_range = "undefined_age"
    if patient_age is None:
        return classified_age_range
    if 0 < patient_age < 15:
        classified_age_range = "children"
    elif 15 <= patient_age < 30:
        classified_age_range = "youth"
    elif 30 <= patient_age < 50:
        classified_age_range = "adults"
    elif patient_age >= 50:
        classified_age_range = "seniors"
    return classified_age_range


def classify_BMI(patient_BMI: float) -> str:
    classified_BMI_range = "undefined_BMI"
    if patient_BMI is None:
        return classified_BMI_range
    if 0.0 < patient_BMI < 18.5:
        classified_BMI_range = "underweight"
    elif 18.5 <= patient_BMI < 25.0:
        classified_BMI_range = "normal-weight"
    elif 25.0 <= patient_BMI < 30.0:
        classified_BMI_range = "overweight"
    elif patient_BMI >= 30.0:
        classified_BMI_range = "obese"
    return classified_BMI_range


def classify_height(patient_height: float) -> str:
    classified_height_range = "undefined_height"
    if patient_height is None:
        return classified_height_range
    if 0.0 < patient_height < 1.6:
        classified_height_range = "short"
    elif 1.6 <= patient_height < 1.8:
        classified_height_range = "average"
    elif 1.8 <= patient_height:
        classified_height_range = "tall"
    return classified_height_range


def stratify_and_standardize_subjects(subjects_directory: str, target_directory: str = None):
    if target_directory is None:
        target_directory = subjects_directory

    subject_directories = file_management.get_subdirectories(subjects_directory)

    cohorts_directory = os.path.join(target_directory, f"stratified_{os.path.basename(subjects_directory)}")
    file_management.create_directory(cohorts_directory)

    for subject_directory in subject_directories:
        DICOM_folders = file_management.get_DICOM_folders(subject_directory)
        subject_folder_name = os.path.basename(subject_directory)

        if len(DICOM_folders) > 0:
            CT_directory = file_management.get_CT_directory(DICOM_folders)
            PET_directory = file_management.get_PET_directory(DICOM_folders)

            if CT_directory is None or PET_directory is None:
                print(f"No PET or CT folders found for subject {subject_folder_name}")
                continue
            patient = Subject(PET_directory)

            cohort_age = classify_age(patient.age)
            cohort_BMI = classify_BMI(patient.BMI)
            cohort_sex = classify_sex(patient.sex)
            cohort_height = classify_height(patient.height)

            cohort_name = f"cohort_{cohort_sex}_{cohort_age}_{cohort_BMI}_{cohort_height}"
            cohort_directory = os.path.join(cohorts_directory, cohort_name)

            file_management.create_directory(cohort_directory)

            subject_cohort_directory = os.path.join(cohort_directory, subject_folder_name)
            file_management.create_directory(subject_cohort_directory)

            print(f"[OCELOT] organizing PET for {subject_folder_name}")
            subject_PET_cohort_DICOM_directory = os.path.join(subject_cohort_directory, f"DICOM_PET_{subject_folder_name}")
            file_management.copy_directory(PET_directory, subject_PET_cohort_DICOM_directory)
            subject_PET_cohort_nifti_path = os.path.join(subject_cohort_directory, f"PET_{subject_folder_name}.nii.gz")
            image_conversion.dicom_to_nifti(subject_PET_cohort_DICOM_directory, subject_PET_cohort_nifti_path)

            print(f"[OCELOT] organizing SUV-PET for {subject_folder_name}")
            subject_SUV_PET_cohort_nifti_path = os.path.join(subject_cohort_directory, f"SUV_PET_{subject_folder_name}.nii.gz")
            image_conversion.bq_PET_to_suv_PET(subject_PET_cohort_nifti_path, subject_SUV_PET_cohort_nifti_path, subject_PET_cohort_DICOM_directory)

            print(f"[OCELOT] organizing CT for {subject_folder_name}")
            subject_CT_cohort_DICOM_directory = os.path.join(subject_cohort_directory, f"DICOM_CT_{subject_folder_name}")
            file_management.copy_directory(CT_directory, subject_CT_cohort_DICOM_directory)
            subject_CT_cohort_nifti_path = os.path.join(subject_cohort_directory, f"CT_{subject_folder_name}.nii.gz")
            image_conversion.dicom_to_nifti(subject_CT_cohort_DICOM_directory, subject_CT_cohort_nifti_path)

        else:
            print(f"No DICOM folders found for subject {subject_folder_name}")
            continue

    number_of_created_cohorts = len(os.listdir(cohorts_directory))
    print(f"[OCELOT] build {number_of_created_cohorts} cohorts from {len(subject_directories)} subjects. ")
    if number_of_created_cohorts == 0:
        print(f"Inspect the contents of the {len(subject_directories)} subject directories!")
