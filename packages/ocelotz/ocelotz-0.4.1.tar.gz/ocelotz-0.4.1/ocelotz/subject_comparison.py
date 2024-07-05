# ------------------------------------------------------ Imports ----------------------------------------------------- #
import os
import SimpleITK
import pandas

from ocelotz import constants as c
from ocelotz import image_processing
from ocelotz import image_analysis
from ocelotz import segmentation_interface
from ocelotz import registration
from ocelotz import file_management
from ocelotz import system


class Tissue:
    def __init__(self, name, label_intensity, label_file_name):
        self.name = name
        self.label_intensity = label_intensity
        self.label_file_name = label_file_name


TISSUE_SEQUENCE = []
for model, labels in segmentation_interface.CLIN_CT_ORGAN_INDICES.items():
    for label_index, label_name in labels.items():
        TISSUE_SEQUENCE.append(Tissue(label_name, label_index, f"{c.FILE_PREFIX_LABEL}{model}.nii.gz"))
TISSUE_SEQUENCE.append(Tissue("residual_tissue", "1", c.RESIDUAL_BODY_MASK_NAME))


def compare_subjects(normative_database_directory: str, subjects_directory: str, clean_up: bool = False, mask_regions: str = None):
    process_start_time = system.set_start_time()
    subject_directories = file_management.get_subdirectories(subjects_directory)
    number_of_subjects = len(subject_directories)

    if number_of_subjects < 1:
        print(f'[OCELOT] requires at least one subject for comparing to NormDB.')
        exit(1)
    else:
        print(f'[OCELOT] found {number_of_subjects} patient(s) to compare to NormDB.')

    # Create OCELOT and comparison directory if it does not already exist
    ocelot_directory = os.path.join(subjects_directory, f'OCELOT')
    file_management.create_directory(ocelot_directory)
    comparison_directory = os.path.join(ocelot_directory, f'comparison')
    file_management.create_directory(comparison_directory)

    normative_database_folder_name = os.path.basename(normative_database_directory)
    normative_database_ocelot_directory = os.path.join(ocelot_directory, normative_database_folder_name)
    file_management.create_directory(normative_database_ocelot_directory)

    if clean_up:
        print(f'[OCELOT] will clean up every subject working directory in {ocelot_directory} after processing.')

    mask_regions = segmentation_interface.regions_string_to_list(mask_regions)
    if mask_regions is not None:
        print(f'[OCELOT] will mask the following regions during comparison: {mask_regions}.')

    # --------------------------------------------------- NormDB ----------------------------------------------------- #
    normative_CT_path = file_management.get_image_path(normative_database_directory, c.FILE_PREFIX_CT)
    normative_PET_path = file_management.get_image_path(normative_database_directory, c.FILE_PREFIX_PET)
    normative_SUV_PET_path = file_management.get_image_path(normative_database_directory, c.FILE_PREFIX_SUV_PET)
    normative_STD_SUV_PET_path = file_management.get_image_path(normative_database_directory, c.FILE_PREFIX_STD_SUV_PET)
    aberration_map_type = c.Z_MAP
    if normative_STD_SUV_PET_path is None:
        normative_STD_SUV_PET_path = normative_SUV_PET_path
        aberration_map_type = c.PERCENTAGE_DIFFERENCE_MAP

    print(f"[OCELOT]    Aberration maps will be: {aberration_map_type}")

    # ------------------------------------------------- Reslicing CT ------------------------------------------------- #
    normative_PET_image = SimpleITK.ReadImage(normative_PET_path)
    normative_CT_image = SimpleITK.ReadImage(normative_CT_path)
    if not image_processing.image_geometries_identical(normative_PET_image, normative_CT_image):
        normative_resliced_CT_path = os.path.join(normative_database_directory, f"{c.FILE_PREFIX_PET_ALIGNED}{os.path.basename(normative_CT_path)}")
        print(f"[OCELOT]    Reslicing reference CT according to PET matrix and spacing: {normative_resliced_CT_path}")
        image_processing.reslice_identity(normative_PET_image, normative_CT_image, normative_resliced_CT_path)
        normative_CT_path = normative_resliced_CT_path

    # -------------------------------------------- Generate Segmentations -------------------------------------------- #
    segmentation_interface.generate_all_required_segmentations(normative_database_directory)
    normative_labels_directory = normative_database_directory
    if mask_regions is not None:
        segmentation_interface.mask_regions(normative_database_directory, mask_regions, normative_database_ocelot_directory)
        normative_labels_directory = normative_database_ocelot_directory

    print(f'[OCELOT] Normative Database or Reference:'
          f'\n[OCELOT]    located at   {normative_database_directory}'
          f'\n[OCELOT]    CT image:    {normative_CT_path}'
          f'\n[OCELOT]    PET image:   {normative_PET_path}'
          f'\n[OCELOT]    SUV image:   {normative_SUV_PET_path}'
          f'\n[OCELOT]    STD image:   {normative_STD_SUV_PET_path}'
          f'\n[OCELOT]    Labels:      {normative_labels_directory}')

    for subject_index, subject_directory in enumerate(subject_directories):
        # ------------------------------------------- Prepare patient data ------------------------------------------- #
        subject_folder_name = os.path.basename(subject_directory)

        if subject_folder_name == "OCELOT":
            continue

        subject_ocelot_directory = os.path.join(ocelot_directory, subject_folder_name)
        file_management.create_directory(subject_ocelot_directory)

        subject_comparison_directory = os.path.join(comparison_directory, subject_folder_name)
        file_management.create_directory(subject_comparison_directory)

        subject_aberration_map_comparison_directory = os.path.join(subject_comparison_directory, 'individual_aberration_maps')
        file_management.create_directory(subject_aberration_map_comparison_directory)

        subject_CT_path = file_management.get_image_path(subject_directory, c.FILE_PREFIX_CT)
        subject_PET_path = file_management.get_image_path(subject_directory, c.FILE_PREFIX_PET)
        subject_SUV_PET_path = file_management.get_image_path(subject_directory, c.FILE_PREFIX_SUV_PET)

        print(f'\n[OCELOT] Next patient to compare:'
              f'\n[OCELOT]    Subject:     {subject_folder_name}'
              f'\n[OCELOT]    located at   {subject_directory}')

        # ----------------------------------------------- Reslicing CT ----------------------------------------------- #
        subject_PET_image = SimpleITK.ReadImage(subject_PET_path)
        subject_CT_image = SimpleITK.ReadImage(subject_CT_path)
        if not image_processing.image_geometries_identical(subject_PET_image, subject_CT_image):
            subject_resliced_CT_path = os.path.join(subject_directory, f"{c.FILE_PREFIX_PET_ALIGNED}{os.path.basename(subject_CT_path)}")
            print(f"[OCELOT]    Reslicing {subject_folder_name} CT according to PET matrix and spacing: {subject_resliced_CT_path}")
            image_processing.reslice_identity(subject_PET_image, subject_CT_image, subject_resliced_CT_path)
            subject_CT_path = subject_resliced_CT_path

        # ------------------------------------------ Generate Segmentations ------------------------------------------ #
        segmentation_interface.generate_all_required_segmentations(subject_directory)
        subject_labels_directory = subject_directory
        if mask_regions is not None:
            segmentation_interface.mask_regions(subject_directory, mask_regions, subject_ocelot_directory)
            subject_labels_directory = subject_ocelot_directory

        print(f'[OCELOT]    CT image:    {subject_CT_path}'
              f'\n[OCELOT]    PET image:   {subject_PET_path}'
              f'\n[OCELOT]    SUV image:   {subject_SUV_PET_path}'
              f'\n[OCELOT]    Labels:      {subject_labels_directory}')

        print(f"[OCELOT]    Computing {aberration_map_type} per organ.")
        subject_individual_tissue_aberration_maps = []

        # ------------------------------------------------- Metrics -------------------------------------------------- #
        volume_metrics = []

        # ------------------------------------------------ Alignment ------------------------------------------------- #
        for TISSUE in TISSUE_SEQUENCE:
            tissue_start_time = system.set_start_time()
            print(f"---------------------------------------------------------------------------------------------------"
                  f"\n[OCELOT]    Processing {TISSUE.name}:")
            completed_alignments = []

            normative_tissue_mask_path = os.path.join(normative_labels_directory, TISSUE.label_file_name)
            normative_tissue_mask_image = SimpleITK.ReadImage(normative_tissue_mask_path, SimpleITK.sitkUInt8)
            extracted_normative_tissue_mask_image = image_processing.extract_label(normative_tissue_mask_image, TISSUE.label_intensity)

            subject_tissue_mask_path = os.path.join(subject_labels_directory, TISSUE.label_file_name)
            subject_tissue_mask_image = SimpleITK.ReadImage(subject_tissue_mask_path, SimpleITK.sitkUInt8)
            extracted_subject_tissue_mask_image = image_processing.extract_label(subject_tissue_mask_image, TISSUE.label_intensity)

            if image_processing.is_empty_segmentation(extracted_normative_tissue_mask_image) or image_processing.is_empty_segmentation(extracted_subject_tissue_mask_image):
                print(f"[OCELOT]    Not enough information.")
                continue

            normative_tissue_directory = os.path.join(normative_database_ocelot_directory, TISSUE.name)
            file_management.create_directory(normative_tissue_directory)
            extracted_normative_tissue_mask_path = os.path.join(normative_tissue_directory, f"reference_{TISSUE.name}.nii.gz")
            SimpleITK.WriteImage(extracted_normative_tissue_mask_image, extracted_normative_tissue_mask_path)

            subject_tissue_directory = os.path.join(subject_ocelot_directory, TISSUE.name)
            file_management.create_directory(subject_tissue_directory)
            extracted_subject_tissue_mask_path = os.path.join(subject_tissue_directory, f"subject_{TISSUE.name}.nii.gz")
            SimpleITK.WriteImage(extracted_subject_tissue_mask_image, extracted_subject_tissue_mask_path)

            normative_label_volume = image_analysis.get_label_volume_metrics(extracted_normative_tissue_mask_image)
            subject_label_volume = image_analysis.get_label_volume_metrics(extracted_subject_tissue_mask_image)
            volume_metrics.append([TISSUE.name, normative_label_volume, subject_label_volume])

            # ----------------------------------------------- Moments ------------------------------------------------ #
            alignment = "moments"
            print(f"[OCELOT]     Aligning [{alignment}] {extracted_subject_tissue_mask_path} -> {extracted_normative_tissue_mask_path}")
            completed_alignments.append(alignment)

            moments_transform_patient_to_normdb_file_path = os.path.join(subject_tissue_directory, f"{TISSUE.name}_"
                                                                         f"{alignment}-transform_patient-to-normdb.mat")
            registration.moments(extracted_normative_tissue_mask_path, extracted_subject_tissue_mask_path, moments_transform_patient_to_normdb_file_path)

            # ------------------------------------------------ Affine ------------------------------------------------ #
            alignment = "affine"
            print(f"[OCELOT]     Aligning [{alignment}] {extracted_subject_tissue_mask_path} -> {extracted_normative_tissue_mask_path}")
            completed_alignments.append(alignment)
            affine_transform_patient_to_normdb_file_path = os.path.join(subject_tissue_directory, f"{TISSUE.name}_"
                                                                        f"{alignment}-transform_patient-to-normdb.mat")
            registration.affine(extracted_normative_tissue_mask_path, extracted_subject_tissue_mask_path, affine_transform_patient_to_normdb_file_path,
                                c.COST_FUNCTION_NMI, moments_transform_patient_to_normdb_file_path)

            # ---------------------------------------------- Deformable ---------------------------------------------- #
            alignment = "deformable"
            print(f"[OCELOT]     Aligning [{alignment}] {extracted_subject_tissue_mask_path} -> {extracted_normative_tissue_mask_path}")
            completed_alignments.append(alignment)

            deformable_transform_patient_to_normdb_file_path = os.path.join(subject_tissue_directory, f"{TISSUE.name}_"
                                                                            f"{alignment}-warp_patient-to-normdb.nii.gz")
            deformable_transform_normdb_to_patient_file_path = os.path.join(subject_tissue_directory, f"{TISSUE.name}_"
                                                                            f"{alignment}-warp_normdb-to-patient.nii.gz")

            registration.deformable(extracted_normative_tissue_mask_path, extracted_subject_tissue_mask_path, deformable_transform_patient_to_normdb_file_path,
                                    c.COST_FUNCTION_SSD, affine_transform_patient_to_normdb_file_path, deformable_transform_normdb_to_patient_file_path)

            # ----------------------------------------------- Reslicing ---------------------------------------------- #
            print(f"[OCELOT]     Reslicing SUV image according to {deformable_transform_patient_to_normdb_file_path}")
            alignments = "-".join(completed_alignments)
            aligned_subject_SUV_PET_path = os.path.join(subject_tissue_directory,
                                                        f"{TISSUE.name}_{alignments}-aligned_subject_SUV-PET.nii.gz")
            registration.reslice_deformable(normative_SUV_PET_path, subject_SUV_PET_path, aligned_subject_SUV_PET_path,
                                            deformable_transform_patient_to_normdb_file_path,
                                            affine_transform_patient_to_normdb_file_path, interpolation_type="LINEAR")

            # --------------------------------------------- Aberration map ------------------------------------------- #
            print(f'[OCELOT] {aberration_map_type} will be generated between'
                  f'\n           {normative_SUV_PET_path}'
                  f'\n           {aligned_subject_SUV_PET_path}')

            normative_SUV_PET_image = SimpleITK.ReadImage(normative_SUV_PET_path, SimpleITK.sitkFloat64)
            patient_SUV_PET_image = SimpleITK.ReadImage(aligned_subject_SUV_PET_path, SimpleITK.sitkFloat64)

            if aberration_map_type == c.Z_MAP:
                normative_STD_SUV_PET_image = SimpleITK.ReadImage(normative_STD_SUV_PET_path)
                aberration_map = image_analysis.compute_z_map(patient_SUV_PET_image, normative_SUV_PET_image, normative_STD_SUV_PET_image)
            else:
                aberration_map = image_analysis.compute_percentage_difference_map(patient_SUV_PET_image, normative_SUV_PET_image)

            aberration_map_image_path = os.path.join(subject_tissue_directory, f"{aberration_map_type}_{TISSUE.name}_{subject_folder_name}_NormDB-aligned.nii.gz")
            SimpleITK.WriteImage(aberration_map, aberration_map_image_path)

            aberration_map_masked_image_path = os.path.join(subject_tissue_directory, f"{aberration_map_type}_{TISSUE.name}-masked_{subject_folder_name}_NormDB-aligned.nii.gz")
            image_processing.mask_image(aberration_map_image_path, extracted_normative_tissue_mask_path, aberration_map_masked_image_path)

            # -------------------------------------------- Inverse Reslice ------------------------------------------- #
            print(f'[OCELOT]   Transforming {aberration_map_type} back into subject space.')
            aligned_subject_SUV_PET_path = os.path.join(subject_aberration_map_comparison_directory, f"{aberration_map_type}_{TISSUE.name}_{subject_folder_name}_subject-aligned.nii.gz")
            registration.reslice_deformable_inverse(subject_SUV_PET_path, aberration_map_image_path, aligned_subject_SUV_PET_path,
                                                    deformable_transform_normdb_to_patient_file_path,
                                                    affine_transform_patient_to_normdb_file_path,
                                                    interpolation_type="LINEAR")

            aberration_map_patient_masked_image_path = os.path.join(subject_aberration_map_comparison_directory, f"{aberration_map_type}_{TISSUE.name}-masked_{subject_folder_name}_subject-aligned.nii.gz")
            image_processing.mask_image(aligned_subject_SUV_PET_path, extracted_subject_tissue_mask_path, aberration_map_patient_masked_image_path)

            subject_individual_tissue_aberration_maps.append(aberration_map_patient_masked_image_path)

            print(f'\n[OCELOT] Tissue processing time: {system.get_processing_time(tissue_start_time, "m")}')

        print(f'[OCELOT] Combining all tissue {aberration_map_type}s.')
        aberration_map_tissues_image_path = os.path.join(subject_comparison_directory, f"{subject_folder_name}_{aberration_map_type}_tissues.nii.gz")
        image_processing.sum_images(subject_individual_tissue_aberration_maps[:-1], aberration_map_tissues_image_path)

        print(f'[OCELOT] Combining all {aberration_map_type}s.')
        aberration_map_complete_image_path = os.path.join(subject_comparison_directory, f"{subject_folder_name}_{aberration_map_type}_complete.nii.gz")
        image_processing.sum_images(subject_individual_tissue_aberration_maps, aberration_map_complete_image_path)

        print(f'[OCELOT] Masking {aberration_map_type}.')
        subject_body_mask_path = os.path.join(subject_labels_directory, c.WHOLE_BODY_MASK_NAME)
        subject_body_skin_mask_path = os.path.join(subject_labels_directory, c.WHOLE_BODY_SKIN_MASK_NAME)
        image_processing.erode_mask(subject_body_mask_path, eroded_mask_path=subject_body_skin_mask_path)

        aberration_map_complete_masked_image_path = os.path.join(subject_comparison_directory, f"{subject_folder_name}_{aberration_map_type}_complete-masked.nii.gz")
        image_processing.mask_image(aberration_map_complete_image_path, subject_body_skin_mask_path, aberration_map_complete_masked_image_path)

        csv_file_path = os.path.join(subject_comparison_directory, f"{subject_folder_name}_volumes.csv")
        print(f'[OCELOT] Saving volumes in {csv_file_path}.')
        volume_dataframe = pandas.DataFrame(volume_metrics, columns=['Label Name', 'Volume Reference [mm³]', 'Volume Subject [mm³]'])
        volume_dataframe.to_csv(csv_file_path, index=False)

        if clean_up:
            print(f'[OCELOT] Removing {subject_folder_name} working directory from {ocelot_directory}.')
            file_management.delete_directory(subject_ocelot_directory)
    if clean_up:
        print(f'[OCELOT] Removing {normative_database_folder_name} working directory from {ocelot_directory}.')
        file_management.delete_directory(normative_database_ocelot_directory)

    print(f'\n[OCELOT] took {system.get_processing_time(process_start_time,"m")} to compare {number_of_subjects} subjects.')
