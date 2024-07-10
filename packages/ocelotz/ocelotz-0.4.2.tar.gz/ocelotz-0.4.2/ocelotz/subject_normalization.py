# ------------------------------------------------------ Imports ----------------------------------------------------- #
import os
import SimpleITK

from ocelotz import constants as c
from ocelotz import system
from ocelotz import image_processing
from ocelotz import registration
from ocelotz import file_management
from ocelotz import image_analysis
from ocelotz import segmentation_interface


def is_valid_subject_directory(subject_directory: str) -> bool:
    ct_exists = False
    pet_exists = False
    suv_pet_exists = False

    subject_files = file_management.get_NIFTI_files(subject_directory)
    for subject_file in subject_files:
        if subject_file.startswith(c.FILE_PREFIX_CT):
            if ct_exists:
                ct_exists = False
            else:
                ct_exists = True
        if subject_file.startswith(c.FILE_PREFIX_PET):
            if pet_exists:
                pet_exists = False
            else:
                pet_exists = True
        if subject_file.startswith(c.FILE_PREFIX_SUV_PET):
            if suv_pet_exists:
                suv_pet_exists = False
            else:
                suv_pet_exists = True

    return ct_exists and pet_exists and suv_pet_exists


def get_valid_subject_directories(subjects_directory: str) -> list:
    subject_directories = file_management.get_subdirectories(subjects_directory)

    valid_subject_directories = []
    for subject_directory in subject_directories:
        if is_valid_subject_directory(subject_directory):
            valid_subject_directories.append(subject_directory)

    print(f'[OCELOT] Found {len(valid_subject_directories)} valid subject folders within provided directory.')
    return valid_subject_directories


def create_template_images(cohort_directory: str, clean_up: bool = False):
    # Get all subject folders within cohort directory
    subject_directories = get_valid_subject_directories(cohort_directory)
    number_of_subjects = len(subject_directories)
    cohort_name = os.path.basename(cohort_directory)

    # Confirm to have at least two subjects
    if number_of_subjects < 2:
        print(f'[OCELOT] requires at least two subject folders.')
        exit(1)
    else:
        print(f'[OCELOT] found {number_of_subjects} subject folders.')

    # List to store all aligned images
    aligned_PET_images = []
    aligned_CT_images = []
    aligned_SUV_PET_images = []

    # Create OCELOT and template directory if it does not already exist
    ocelot_directory = os.path.join(cohort_directory, f'OCELOT')
    file_management.create_directory(ocelot_directory)
    template_generation_directory = os.path.join(ocelot_directory, f'template-generation')
    file_management.create_directory(template_generation_directory)

    if clean_up:
        print(f'[OCELOT] will remove template creation directory {template_generation_directory} after processing.')

    total_time_start = system.set_start_time()

    # --------------------------------------------- CT to PET alignment ---------------------------------------------- #
    print(f"\n[OCELOT] Initial CT alignment")
    for subject_index, subject_directory in enumerate(subject_directories):
        # ----------------------------------------------- Needed paths ----------------------------------------------- #
        subject_folder_name = os.path.basename(subject_directory)
        subject_CT_path = file_management.get_image_path(subject_directory, c.FILE_PREFIX_CT)
        subject_PET_path = file_management.get_image_path(subject_directory, c.FILE_PREFIX_PET)

        subject_ocelot_directory = os.path.join(template_generation_directory, subject_folder_name)
        file_management.create_directory(subject_ocelot_directory)

        print(f'[OCELOT] Reslicing CT image of subject {subject_folder_name}:'
              f'\n[OCELOT]    located at   {subject_directory}'
              f'\n[OCELOT]    CT image:    {subject_CT_path}'
              f'\n[OCELOT]    PET image:   {subject_PET_path}')

        subject_resliced_CT_path = os.path.join(subject_ocelot_directory, f"{c.FILE_PREFIX_CT_PET_ALIGNED}subject{subject_index}.nii.gz")

        # ------------------------------------------------ Alignment ------------------------------------------------- #
        subject_PET_image = SimpleITK.ReadImage(subject_PET_path)
        subject_CT_image = SimpleITK.ReadImage(subject_CT_path)
        if not image_processing.image_geometries_identical(subject_PET_image, subject_CT_image):
            print(f"[OCELOT]    Reslicing {subject_folder_name} CT according to PET matrix and spacing: {subject_resliced_CT_path}")
            image_processing.reslice_identity(subject_PET_image, subject_CT_image, subject_resliced_CT_path)
        else:
            file_management.copy_file(subject_CT_path, subject_resliced_CT_path)

    # ------------------------------------------- Inter-patient alignment -------------------------------------------- #
    iteration_CT_template = None
    iteration_PET_template = None
    iteration_SUV_PET_template = None
    iteration_STD_SUV_PET_template = None

    # ---------------------------------------------- Affine alignment ------------------------------------------------ #
    print(f"\n[OCELOT] Initial template creation: Affine")

    for subject_index, subject_directory in enumerate(subject_directories):
        start_time = system.set_start_time()

        # ----------------------------------------------- Needed paths ----------------------------------------------- #
        subject_folder_name = os.path.basename(subject_directory)

        subject_ocelot_directory = os.path.join(template_generation_directory, subject_folder_name)
        file_management.create_directory(subject_ocelot_directory)

        subject_CT_path = file_management.get_image_path(subject_ocelot_directory, c.FILE_PREFIX_CT_PET_ALIGNED)
        subject_PET_path = file_management.get_image_path(subject_directory, c.FILE_PREFIX_PET)
        subject_SUV_PET_path = file_management.get_image_path(subject_directory, c.FILE_PREFIX_SUV_PET)

        aligned_subject_CT_path = os.path.join(subject_ocelot_directory,
                                               f"0_affine_aligned_{c.FILE_PREFIX_CT_PET_ALIGNED}subject{subject_index}.nii.gz")
        aligned_subject_PET_path = os.path.join(subject_ocelot_directory,
                                                f"0_affine_aligned_{c.FILE_PREFIX_PET}subject{subject_index}.nii.gz")
        aligned_subject_SUV_PET_path = os.path.join(subject_ocelot_directory,
                                                    f"0_affine_aligned_{c.FILE_PREFIX_SUV_PET}subject{subject_index}.nii.gz")

        # -------------------------------------------- Reference subject --------------------------------------------- #
        if iteration_CT_template is None and iteration_PET_template is None and iteration_SUV_PET_template is None:
            print(f'[OCELOT] Target subject to base template image on: {subject_directory}'
                  f'\n[OCELOT]    located at   {subject_folder_name}'
                  f'\n[OCELOT]    CT image:    {subject_CT_path}'
                  f'\n[OCELOT]    PET image:   {subject_PET_path}')

            file_management.copy_file(subject_CT_path, aligned_subject_CT_path)
            iteration_CT_template = aligned_subject_CT_path

            file_management.copy_file(subject_PET_path, aligned_subject_PET_path)
            iteration_PET_template = aligned_subject_PET_path

            file_management.copy_file(subject_SUV_PET_path, aligned_subject_SUV_PET_path)
            iteration_SUV_PET_template = aligned_subject_SUV_PET_path

        # --------------------------------------------- Subject to align --------------------------------------------- #
        else:
            print(f'[OCELOT] Next subject to align: {subject_directory}'
                  f'\n[OCELOT]    located at   {subject_folder_name}'
                  f'\n[OCELOT]    CT image:    {subject_CT_path}'
                  f'\n[OCELOT]    PET image:   {subject_PET_path}')

            # ---------------------------------------------- Alignment ----------------------------------------------- #
            print(f"[OCELOT]    Aligning affine: {subject_CT_path} -> {iteration_CT_template}")
            initial_transform_file_path = os.path.join(subject_ocelot_directory, "0_initial_transform.mat")
            registration.affine(iteration_CT_template, subject_CT_path, initial_transform_file_path, c.COST_FUNCTION_NMI)

            print(f"[OCELOT]    Reslicing CT according to {initial_transform_file_path}")
            registration.reslice_affine(iteration_CT_template, subject_CT_path, aligned_subject_CT_path,
                                        initial_transform_file_path, interpolation_type="LINEAR")

            print(f"[OCELOT]    Reslicing PET according to {initial_transform_file_path}")
            registration.reslice_affine(iteration_PET_template, subject_PET_path, aligned_subject_PET_path,
                                        initial_transform_file_path, interpolation_type="LINEAR")

            print(f"[OCELOT]    Reslicing SUV PET according to {initial_transform_file_path}")
            registration.reslice_affine(iteration_SUV_PET_template, subject_SUV_PET_path, aligned_subject_SUV_PET_path,
                                        initial_transform_file_path, interpolation_type="LINEAR")

        aligned_CT_images.append(aligned_subject_CT_path)
        aligned_PET_images.append(aligned_subject_PET_path)
        aligned_SUV_PET_images.append(aligned_subject_SUV_PET_path)

        print(f'[OCELOT]    Subject processing took {system.get_processing_time(start_time, "m")}.')

    print(f'[OCELOT] Averaging CT images.')
    average_affine_CT_image = os.path.join(template_generation_directory, f"0_affine_average_cohort_{c.FILE_PREFIX_CT_PET_ALIGNED}N"
                                           f"{len(aligned_CT_images)}.nii.gz")
    image_processing.average_images(aligned_CT_images, average_affine_CT_image)
    aligned_CT_images.clear()
    iteration_CT_template = average_affine_CT_image

    print(f'[OCELOT] Averaging PET images.')
    average_affine_PET_image = os.path.join(template_generation_directory, f"0_affine_average_cohort_{c.FILE_PREFIX_PET}N"
                                            f"{len(aligned_PET_images)}.nii.gz")
    image_processing.average_images(aligned_PET_images, average_affine_PET_image)
    aligned_PET_images.clear()
    iteration_PET_template = average_affine_PET_image

    print(f'[OCELOT] Averaging SUV PET images.')
    average_affine_SUV_PET_image = os.path.join(template_generation_directory, f"0_affine_average_cohort_{c.FILE_PREFIX_SUV_PET}N"
                                                f"{len(aligned_SUV_PET_images)}.nii.gz")
    image_processing.average_images(aligned_SUV_PET_images, average_affine_SUV_PET_image)
    aligned_SUV_PET_images.clear()
    iteration_SUV_PET_template = average_affine_SUV_PET_image

    # -------------------------------------------- Deformable alignment ---------------------------------------------- #
    print(f"\n[OCELOT] Initial template creation: Iterative deformable")

    for template_iteration in range(1, c.NUMBER_OF_DEFORMABLE_ITERATIONS + 1):
        print(f'[OCELOT] Template iteration {template_iteration}')
        print(f'[OCELOT] Target CT for this iteration is:  {iteration_CT_template}')
        print(f'[OCELOT] Target PET for this iteration is: {iteration_PET_template}')
        print(f'[OCELOT] Target SUV PET for this iteration is: {iteration_SUV_PET_template}')

        for subject_index, subject_directory in enumerate(subject_directories):
            start_time = system.set_start_time()

            # --------------------------------------------- Needed paths --------------------------------------------- #
            subject_folder_name = os.path.basename(subject_directory)

            # ------------------------------------------- Subject to align ------------------------------------------- #
            subject_template_directory = os.path.join(template_generation_directory, subject_folder_name)
            subject_CT_path = os.path.join(subject_template_directory, f"0_affine_aligned_{c.FILE_PREFIX_CT_PET_ALIGNED}subject"
                                                                       f"{subject_index}.nii.gz")
            subject_PET_path = os.path.join(subject_template_directory, f"0_affine_aligned_{c.FILE_PREFIX_PET}subject"
                                                                        f"{subject_index}.nii.gz")
            subject_SUV_PET_path = os.path.join(subject_template_directory, f"0_affine_aligned_{c.FILE_PREFIX_SUV_PET}subject"
                                                                            f"{subject_index}.nii.gz")

            print(f'[OCELOT] Next subject to align: {subject_directory}'
                  f'\n[OCELOT]    located at   {subject_folder_name}'
                  f'\n[OCELOT]    CT image:    {subject_CT_path}'
                  f'\n[OCELOT]    PET image:   {subject_PET_path}')

            aligned_subject_CT_path = os.path.join(subject_template_directory,
                                                   f"{template_iteration}_deformable_aligned_{c.FILE_PREFIX_CT_PET_ALIGNED}subject"
                                                   f"{subject_index}.nii.gz")
            aligned_subject_PET_path = os.path.join(subject_template_directory,
                                                    f"{template_iteration}_deformable_aligned_{c.FILE_PREFIX_PET}subject"
                                                    f"{subject_index}.nii.gz")
            aligned_subject_SUV_PET_path = os.path.join(subject_template_directory,
                                                        f"{template_iteration}_deformable_aligned_{c.FILE_PREFIX_SUV_PET}subject"
                                                        f"{subject_index}.nii.gz")

            # ---------------------------------------------- Alignment ----------------------------------------------- #
            print(f"[OCELOT]    Aligning deformable: {subject_CT_path} -> {iteration_CT_template}")
            deformable_transform_file_path = os.path.join(subject_template_directory, f"{template_iteration}_deformable_warp.nii.gz")
            registration.deformable(iteration_CT_template, subject_CT_path, deformable_transform_file_path, c.COST_FUNCTION_SSD)

            print(f"[OCELOT]    Reslicing CT according to {deformable_transform_file_path}")
            registration.reslice_deformable(iteration_CT_template, subject_CT_path, aligned_subject_CT_path,
                                            deformable_transform_file_path, interpolation_type="LINEAR")
            aligned_CT_images.append(aligned_subject_CT_path)

            print(f"[OCELOT]    Reslicing PET according to {deformable_transform_file_path}")
            registration.reslice_deformable(iteration_PET_template, subject_PET_path, aligned_subject_PET_path,
                                            deformable_transform_file_path, interpolation_type="LINEAR")
            aligned_PET_images.append(aligned_subject_PET_path)

            print(f"[OCELOT]    Reslicing SUV PET according to {deformable_transform_file_path}")
            registration.reslice_deformable(iteration_SUV_PET_template, subject_SUV_PET_path, aligned_subject_SUV_PET_path,
                                            deformable_transform_file_path, interpolation_type="LINEAR")
            aligned_SUV_PET_images.append(aligned_subject_SUV_PET_path)

            print(f'[OCELOT]    Subject processing took {system.get_processing_time(start_time, "m")}.')

        print(f'[OCELOT] Averaging CT images.')
        average_CT_image = os.path.join(template_generation_directory,
                                        f"{template_iteration}_deformed_average_cohort_{c.FILE_PREFIX_CT_PET_ALIGNED}N"
                                        f"{len(aligned_CT_images)}.nii.gz")
        image_processing.average_images(aligned_CT_images, average_CT_image)
        iteration_CT_template = average_CT_image
        aligned_CT_images.clear()

        print(f'[OCELOT] Averaging PET images.')
        average_PET_image = os.path.join(template_generation_directory,
                                         f"{template_iteration}_deformed_average_cohort_{c.FILE_PREFIX_PET}N"
                                         f"{len(aligned_PET_images)}.nii.gz")
        image_processing.average_images(aligned_PET_images, average_PET_image)
        iteration_PET_template = average_PET_image
        aligned_PET_images.clear()

        print(f'[OCELOT] Averaging SUV PET images.')
        average_SUV_PET_image = os.path.join(template_generation_directory,
                                             f"{template_iteration}_deformed_average_cohort_{c.FILE_PREFIX_SUV_PET}N"
                                             f"{len(aligned_SUV_PET_images)}.nii.gz")
        mean_SUV_PET = image_processing.average_images(aligned_SUV_PET_images, average_SUV_PET_image)
        iteration_SUV_PET_template = average_SUV_PET_image

        print(f'[OCELOT] Computing STD SUV PET images.')
        std_SUV_PET_image = os.path.join(template_generation_directory,
                                         f"{template_iteration}_deformed_average_cohort_STD_{c.FILE_PREFIX_SUV_PET}N"
                                         f"{len(aligned_SUV_PET_images)}.nii.gz")
        image_analysis.std_images(aligned_SUV_PET_images, mean_SUV_PET, std_SUV_PET_image)
        iteration_STD_SUV_PET_template = std_SUV_PET_image
        aligned_SUV_PET_images.clear()

        print(f"")

    print(f'[OCELOT] Template creation took {system.get_processing_time(total_time_start, "m")}.')

    # ------------------------------------------- NormDB folder creation --------------------------------------------- #
    print(f'\n[OCELOT] Storing normative template images in:')
    database_directory = os.path.join(ocelot_directory, f'NormDB_'
                                                        f'N{number_of_subjects}-subjects_'
                                                        f'N{c.NUMBER_OF_DEFORMABLE_ITERATIONS + 1}-iterations_'
                                                        f'{cohort_name}')
    file_management.create_directory(database_directory)
    print(f'[OCELOT] {database_directory}')

    database_CT_path = os.path.join(database_directory, f"{c.FILE_PREFIX_CT}template_{cohort_name}.nii.gz")
    file_management.copy_file(iteration_CT_template, database_CT_path)

    database_PET_path = os.path.join(database_directory, f"{c.FILE_PREFIX_PET}template_{cohort_name}.nii.gz")
    file_management.copy_file(iteration_PET_template, database_PET_path)

    database_SUV_PET_path = os.path.join(database_directory, f"{c.FILE_PREFIX_SUV_PET}template_{cohort_name}.nii.gz")
    file_management.copy_file(iteration_SUV_PET_template, database_SUV_PET_path)

    database_STD_SUV_PET_path = os.path.join(database_directory, f"{c.FILE_PREFIX_STD_SUV_PET}template_{cohort_name}.nii.gz")
    file_management.copy_file(iteration_STD_SUV_PET_template, database_STD_SUV_PET_path)

    print(f'[OCELOT] Creating segmentations:')
    segmentation_interface.generate_all_required_segmentations(database_directory)

    if clean_up:
        print(f'[OCELOT] Removing {template_generation_directory} working directory from {ocelot_directory}.')
        file_management.delete_directory(template_generation_directory)


AFFINE_ITERATIONS = 3
DEFORMABLE_ITERATIONS = 5


def create_template_images_EXPERIMENTAL(cohort_directory: str, clean_up: bool = False):
    subject_directories = get_valid_subject_directories(cohort_directory)
    number_of_subjects = len(subject_directories)
    cohort_name = os.path.basename(cohort_directory)

    # Confirm to have at least two subjects
    if number_of_subjects < 2:
        print(f'[OCELOT] requires at least two subject folders.')
        exit(1)
    else:
        print(f'[OCELOT] found {number_of_subjects} subject folders.')

    # List to store all aligned images
    aligned_PET_images = []
    aligned_CT_images = []
    aligned_SUV_PET_images = []

    # Create OCELOT and template directory if it does not already exist
    ocelot_directory = os.path.join(cohort_directory, f'OCELOT')
    file_management.create_directory(ocelot_directory)
    template_generation_directory = os.path.join(ocelot_directory, f'template-generation')
    file_management.create_directory(template_generation_directory)

    if clean_up:
        print(f'[OCELOT] will remove template creation directory {template_generation_directory} after processing.')

    total_time_start = system.set_start_time()

    # --------------------------------------------- CT to PET alignment ---------------------------------------------- #
    print(f"\n[OCELOT] Initial CT alignment")
    for subject_index, subject_directory in enumerate(subject_directories):
        # ----------------------------------------------- Needed paths ----------------------------------------------- #
        subject_folder_name = os.path.basename(subject_directory)
        subject_CT_path = file_management.get_image_path(subject_directory, c.FILE_PREFIX_CT)
        subject_PET_path = file_management.get_image_path(subject_directory, c.FILE_PREFIX_PET)

        subject_ocelot_directory = os.path.join(template_generation_directory, subject_folder_name)
        file_management.create_directory(subject_ocelot_directory)

        print(f'[OCELOT] Reslicing CT image of subject {subject_folder_name}:'
              f'\n[OCELOT]    located at   {subject_directory}'
              f'\n[OCELOT]    CT image:    {subject_CT_path}'
              f'\n[OCELOT]    PET image:   {subject_PET_path}')

        subject_resliced_CT_path = os.path.join(subject_ocelot_directory, f"{c.FILE_PREFIX_CT_PET_ALIGNED}subject{subject_index}.nii.gz")

        # ------------------------------------------------ Alignment ------------------------------------------------- #
        subject_PET_image = SimpleITK.ReadImage(subject_PET_path)
        subject_CT_image = SimpleITK.ReadImage(subject_CT_path)
        if not image_processing.image_geometries_identical(subject_PET_image, subject_CT_image):
            print(f"[OCELOT]    Reslicing {subject_folder_name} CT according to PET matrix and spacing: {subject_resliced_CT_path}")
            image_processing.reslice_identity(subject_PET_image, subject_CT_image, subject_resliced_CT_path)
        else:
            file_management.copy_file(subject_CT_path, subject_resliced_CT_path)

        print(f"[OCELOT]    Masking {subject_folder_name} CT according to body mask.")
        subject_resliced_masked_CT_path = os.path.join(subject_ocelot_directory, f"{c.FILE_PREFIX_CT_PET_ALIGNED_MASKED}subject{subject_index}.nii.gz")
        segmentation_interface.body_mask_image(subject_resliced_CT_path, subject_resliced_masked_CT_path)

    # ------------------------------------------- Inter-patient alignment -------------------------------------------- #
    iteration_CT_template = None
    iteration_PET_template = None
    iteration_SUV_PET_template = None
    iteration_STD_SUV_PET_template = None

    # ---------------------------------------------- Rigid alignment ------------------------------------------------- #
    print(f"\n[OCELOT] Initial template creation: rigid")
    alignment_iteration = 0
    for subject_index, subject_directory in enumerate(subject_directories):
        start_time = system.set_start_time()

        # ----------------------------------------------- Needed paths ----------------------------------------------- #
        subject_folder_name = os.path.basename(subject_directory)

        subject_ocelot_directory = os.path.join(template_generation_directory, subject_folder_name)
        file_management.create_directory(subject_ocelot_directory)

        subject_CT_path = file_management.get_image_path(subject_ocelot_directory, c.FILE_PREFIX_CT_PET_ALIGNED_MASKED)
        subject_PET_path = file_management.get_image_path(subject_directory, c.FILE_PREFIX_PET)
        subject_SUV_PET_path = file_management.get_image_path(subject_directory, c.FILE_PREFIX_SUV_PET)

        aligned_subject_CT_path = os.path.join(subject_ocelot_directory,
                                               f"{alignment_iteration}_rigid_aligned_{c.FILE_PREFIX_CT_PET_ALIGNED_MASKED}subject{subject_index}.nii.gz")
        aligned_subject_PET_path = os.path.join(subject_ocelot_directory,
                                                f"{alignment_iteration}_rigid_aligned_{c.FILE_PREFIX_PET}subject{subject_index}.nii.gz")
        aligned_subject_SUV_PET_path = os.path.join(subject_ocelot_directory,
                                                    f"{alignment_iteration}_rigid_aligned_{c.FILE_PREFIX_SUV_PET}subject{subject_index}.nii.gz")

        # -------------------------------------------- Reference subject --------------------------------------------- #
        if iteration_CT_template is None and iteration_PET_template is None and iteration_SUV_PET_template is None:
            print(f'[OCELOT] Target subject to base template image on: {subject_directory}'
                  f'\n[OCELOT]    located at   {subject_folder_name}'
                  f'\n[OCELOT]    CT image:    {subject_CT_path}'
                  f'\n[OCELOT]    PET image:   {subject_PET_path}')

            file_management.copy_file(subject_CT_path, aligned_subject_CT_path)
            iteration_CT_template = aligned_subject_CT_path

            file_management.copy_file(subject_PET_path, aligned_subject_PET_path)
            iteration_PET_template = aligned_subject_PET_path

            file_management.copy_file(subject_SUV_PET_path, aligned_subject_SUV_PET_path)
            iteration_SUV_PET_template = aligned_subject_SUV_PET_path

        # --------------------------------------------- Subject to align --------------------------------------------- #
        else:
            print(f'[OCELOT] Next subject to align: {subject_directory}'
                  f'\n[OCELOT]    located at   {subject_folder_name}'
                  f'\n[OCELOT]    CT image:    {subject_CT_path}'
                  f'\n[OCELOT]    PET image:   {subject_PET_path}')

            # ---------------------------------------------- Alignment ----------------------------------------------- #
            print(f"[OCELOT]    Aligning rigid: {subject_CT_path} -> {iteration_CT_template}")
            initial_transform_file_path = os.path.join(subject_ocelot_directory, f"{alignment_iteration}_rigid_transform.mat")
            registration.affine(iteration_CT_template, subject_CT_path, initial_transform_file_path, c.COST_FUNCTION_NMI)

            print(f"[OCELOT]    Reslicing CT according to {initial_transform_file_path}")
            registration.reslice_affine(iteration_CT_template, subject_CT_path, aligned_subject_CT_path,
                                        initial_transform_file_path, interpolation_type="LINEAR", background=c.CT_BACKGROUND_VALUE)

            print(f"[OCELOT]    Reslicing PET according to {initial_transform_file_path}")
            registration.reslice_affine(iteration_PET_template, subject_PET_path, aligned_subject_PET_path,
                                        initial_transform_file_path, interpolation_type="LINEAR")

            print(f"[OCELOT]    Reslicing SUV PET according to {initial_transform_file_path}")
            registration.reslice_affine(iteration_SUV_PET_template, subject_SUV_PET_path, aligned_subject_SUV_PET_path,
                                        initial_transform_file_path, interpolation_type="LINEAR")

        aligned_CT_images.append(aligned_subject_CT_path)
        aligned_PET_images.append(aligned_subject_PET_path)
        aligned_SUV_PET_images.append(aligned_subject_SUV_PET_path)

        print(f'[OCELOT]    Subject processing took {system.get_processing_time(start_time, "m")}.')

    print(f'[OCELOT] Averaging CT images.')
    average_rigid_CT_image = os.path.join(template_generation_directory, f"{alignment_iteration}_rigid_average_cohort_{c.FILE_PREFIX_CT_PET_ALIGNED_MASKED}N"
                                          f"{len(aligned_CT_images)}.nii.gz")
    image_processing.average_images(aligned_CT_images, average_rigid_CT_image)
    aligned_CT_images.clear()
    iteration_CT_template = average_rigid_CT_image

    print(f'[OCELOT] Averaging PET images.')
    average_rigid_PET_image = os.path.join(template_generation_directory, f"{alignment_iteration}_rigid_average_cohort_{c.FILE_PREFIX_PET}N"
                                           f"{len(aligned_PET_images)}.nii.gz")
    image_processing.average_images(aligned_PET_images, average_rigid_PET_image)
    aligned_PET_images.clear()
    iteration_PET_template = average_rigid_PET_image

    print(f'[OCELOT] Averaging SUV PET images.')
    average_rigid_SUV_PET_image = os.path.join(template_generation_directory, f"{alignment_iteration}_rigid_average_cohort_{c.FILE_PREFIX_SUV_PET}N"
                                               f"{len(aligned_SUV_PET_images)}.nii.gz")
    image_processing.average_images(aligned_SUV_PET_images, average_rigid_SUV_PET_image)
    aligned_SUV_PET_images.clear()
    iteration_SUV_PET_template = average_rigid_SUV_PET_image

    # -------------------------------------------- Affine alignment ---------------------------------------------- #
    print(f"\n[OCELOT] Initial template creation: Iterative affine")

    for template_iteration in range(AFFINE_ITERATIONS):
        alignment_iteration += 1
        print(f'[OCELOT] Template iteration {alignment_iteration}')
        print(f'[OCELOT] Target CT for this iteration is:  {iteration_CT_template}')
        print(f'[OCELOT] Target PET for this iteration is: {iteration_PET_template}')
        print(f'[OCELOT] Target SUV PET for this iteration is: {iteration_SUV_PET_template}')

        for subject_index, subject_directory in enumerate(subject_directories):
            start_time = system.set_start_time()

            # --------------------------------------------- Needed paths --------------------------------------------- #
            subject_folder_name = os.path.basename(subject_directory)

            # ------------------------------------------- Subject to align ------------------------------------------- #
            subject_template_directory = os.path.join(template_generation_directory, subject_folder_name)
            subject_CT_path = os.path.join(subject_template_directory,
                                           f"0_rigid_aligned_{c.FILE_PREFIX_CT_PET_ALIGNED_MASKED}subject{subject_index}.nii.gz")
            subject_PET_path = os.path.join(subject_template_directory,
                                            f"0_rigid_aligned_{c.FILE_PREFIX_PET}subject{subject_index}.nii.gz")
            subject_SUV_PET_path = os.path.join(subject_template_directory,
                                                f"0_rigid_aligned_{c.FILE_PREFIX_SUV_PET}subject{subject_index}.nii.gz")

            print(f'[OCELOT] Next subject to align: {subject_directory}'
                  f'\n[OCELOT]    located at   {subject_folder_name}'
                  f'\n[OCELOT]    CT image:    {subject_CT_path}'
                  f'\n[OCELOT]    PET image:   {subject_PET_path}')

            aligned_subject_CT_path = os.path.join(subject_template_directory,
                                                   f"{alignment_iteration}_affine_aligned_{c.FILE_PREFIX_CT_PET_ALIGNED_MASKED}subject"
                                                   f"{subject_index}.nii.gz")
            aligned_subject_PET_path = os.path.join(subject_template_directory,
                                                    f"{alignment_iteration}_affine_aligned_{c.FILE_PREFIX_PET}subject"
                                                    f"{subject_index}.nii.gz")
            aligned_subject_SUV_PET_path = os.path.join(subject_template_directory,
                                                        f"{alignment_iteration}_affine_aligned_{c.FILE_PREFIX_SUV_PET}subject"
                                                        f"{subject_index}.nii.gz")

            # ---------------------------------------------- Alignment ----------------------------------------------- #
            print(f"[OCELOT]    Aligning affine: {subject_CT_path} -> {iteration_CT_template}")
            affine_transform_file_path = os.path.join(subject_template_directory, f"{alignment_iteration}_affine_transform.nii.gz")
            registration.deformable(iteration_CT_template, subject_CT_path, affine_transform_file_path,
                                    c.COST_FUNCTION_SSD)

            print(f"[OCELOT]    Reslicing CT according to {affine_transform_file_path}")
            registration.reslice_affine(iteration_CT_template, subject_CT_path, aligned_subject_CT_path,
                                        affine_transform_file_path, interpolation_type="LINEAR", background=c.CT_BACKGROUND_VALUE)
            aligned_CT_images.append(aligned_subject_CT_path)

            print(f"[OCELOT]    Reslicing PET according to {affine_transform_file_path}")
            registration.reslice_affine(iteration_PET_template, subject_PET_path, aligned_subject_PET_path,
                                        affine_transform_file_path, interpolation_type="LINEAR")
            aligned_PET_images.append(aligned_subject_PET_path)

            print(f"[OCELOT]    Reslicing SUV PET according to {affine_transform_file_path}")
            registration.reslice_affine(iteration_SUV_PET_template, subject_SUV_PET_path, aligned_subject_SUV_PET_path,
                                        affine_transform_file_path, interpolation_type="LINEAR")
            aligned_SUV_PET_images.append(aligned_subject_SUV_PET_path)

            print(f'[OCELOT]    Subject processing took {system.get_processing_time(start_time, "m")}.')

        print(f'[OCELOT] Averaging CT images.')
        average_CT_image = os.path.join(template_generation_directory,
                                        f"{alignment_iteration}_affine_average_cohort_{c.FILE_PREFIX_CT_PET_ALIGNED_MASKED}N"
                                        f"{len(aligned_CT_images)}.nii.gz")
        image_processing.average_images(aligned_CT_images, average_CT_image)
        iteration_CT_template = average_CT_image
        aligned_CT_images.clear()

        print(f'[OCELOT] Averaging PET images.')
        average_PET_image = os.path.join(template_generation_directory,
                                         f"{alignment_iteration}_affine_average_cohort_{c.FILE_PREFIX_PET}N"
                                         f"{len(aligned_PET_images)}.nii.gz")
        image_processing.average_images(aligned_PET_images, average_PET_image)
        iteration_PET_template = average_PET_image
        aligned_PET_images.clear()

        print(f'[OCELOT] Averaging SUV PET images.')
        average_SUV_PET_image = os.path.join(template_generation_directory,
                                             f"{alignment_iteration}_affine_average_cohort_{c.FILE_PREFIX_SUV_PET}N"
                                             f"{len(aligned_SUV_PET_images)}.nii.gz")
        mean_SUV_PET = image_processing.average_images(aligned_SUV_PET_images, average_SUV_PET_image)
        iteration_SUV_PET_template = average_SUV_PET_image

        print(f'[OCELOT] Computing STD SUV PET images.')
        std_SUV_PET_image = os.path.join(template_generation_directory,
                                         f"{alignment_iteration}_affine_average_cohort_STD_{c.FILE_PREFIX_SUV_PET}N"
                                         f"{len(aligned_SUV_PET_images)}.nii.gz")
        image_analysis.std_images(aligned_SUV_PET_images, mean_SUV_PET, std_SUV_PET_image)
        iteration_STD_SUV_PET_template = std_SUV_PET_image
        aligned_SUV_PET_images.clear()

    # -------------------------------------------- Deformable alignment ---------------------------------------------- #
    print(f"\n[OCELOT] Initial template creation: Iterative deformable")

    for template_iteration in range(DEFORMABLE_ITERATIONS):
        alignment_iteration += 1
        print(f'[OCELOT] Template iteration {alignment_iteration}')
        print(f'[OCELOT] Target CT for this iteration is:  {iteration_CT_template}')
        print(f'[OCELOT] Target PET for this iteration is: {iteration_PET_template}')
        print(f'[OCELOT] Target SUV PET for this iteration is: {iteration_SUV_PET_template}')

        for subject_index, subject_directory in enumerate(subject_directories):
            start_time = system.set_start_time()

            # --------------------------------------------- Needed paths --------------------------------------------- #
            subject_folder_name = os.path.basename(subject_directory)

            # ------------------------------------------- Subject to align ------------------------------------------- #
            subject_template_directory = os.path.join(template_generation_directory, subject_folder_name)
            subject_CT_path = os.path.join(subject_template_directory, f"0_rigid_aligned_{c.FILE_PREFIX_CT_PET_ALIGNED_MASKED}subject"
                                                                       f"{subject_index}.nii.gz")
            subject_PET_path = os.path.join(subject_template_directory, f"0_rigid_aligned_{c.FILE_PREFIX_PET}subject"
                                                                        f"{subject_index}.nii.gz")
            subject_SUV_PET_path = os.path.join(subject_template_directory, f"0_rigid_aligned_{c.FILE_PREFIX_SUV_PET}subject"
                                                                            f"{subject_index}.nii.gz")

            print(f'[OCELOT] Next subject to align: {subject_directory}'
                  f'\n[OCELOT]    located at   {subject_folder_name}'
                  f'\n[OCELOT]    CT image:    {subject_CT_path}'
                  f'\n[OCELOT]    PET image:   {subject_PET_path}')

            aligned_subject_CT_path = os.path.join(subject_template_directory,
                                                   f"{alignment_iteration}_deformable_aligned_{c.FILE_PREFIX_CT_PET_ALIGNED_MASKED}subject"
                                                   f"{subject_index}.nii.gz")
            aligned_subject_PET_path = os.path.join(subject_template_directory,
                                                    f"{alignment_iteration}_deformable_aligned_{c.FILE_PREFIX_PET}subject"
                                                    f"{subject_index}.nii.gz")
            aligned_subject_SUV_PET_path = os.path.join(subject_template_directory,
                                                        f"{alignment_iteration}_deformable_aligned_{c.FILE_PREFIX_SUV_PET}subject"
                                                        f"{subject_index}.nii.gz")

            # ---------------------------------------------- Alignment ----------------------------------------------- #
            print(f"[OCELOT]    Aligning deformable: {subject_CT_path} -> {iteration_CT_template}")
            deformable_transform_file_path = os.path.join(subject_template_directory, f"{alignment_iteration}_deformable_warp.nii.gz")
            registration.deformable(iteration_CT_template, subject_CT_path, deformable_transform_file_path, c.COST_FUNCTION_SSD)

            print(f"[OCELOT]    Reslicing CT according to {deformable_transform_file_path}")
            registration.reslice_deformable(iteration_CT_template, subject_CT_path, aligned_subject_CT_path,
                                            deformable_transform_file_path, interpolation_type="LINEAR", background=c.CT_BACKGROUND_VALUE)
            aligned_CT_images.append(aligned_subject_CT_path)

            print(f"[OCELOT]    Reslicing PET according to {deformable_transform_file_path}")
            registration.reslice_deformable(iteration_PET_template, subject_PET_path, aligned_subject_PET_path,
                                            deformable_transform_file_path, interpolation_type="LINEAR")
            aligned_PET_images.append(aligned_subject_PET_path)

            print(f"[OCELOT]    Reslicing SUV PET according to {deformable_transform_file_path}")
            registration.reslice_deformable(iteration_SUV_PET_template, subject_SUV_PET_path, aligned_subject_SUV_PET_path,
                                            deformable_transform_file_path, interpolation_type="LINEAR")
            aligned_SUV_PET_images.append(aligned_subject_SUV_PET_path)

            print(f'[OCELOT]    Subject processing took {system.get_processing_time(start_time, "m")}.')

        print(f'[OCELOT] Averaging CT images.')
        average_CT_image = os.path.join(template_generation_directory,
                                        f"{alignment_iteration}_deformed_average_cohort_{c.FILE_PREFIX_CT_PET_ALIGNED_MASKED}N"
                                        f"{len(aligned_CT_images)}.nii.gz")
        image_processing.average_images(aligned_CT_images, average_CT_image)
        iteration_CT_template = average_CT_image
        aligned_CT_images.clear()

        print(f'[OCELOT] Averaging PET images.')
        average_PET_image = os.path.join(template_generation_directory,
                                         f"{alignment_iteration}_deformed_average_cohort_{c.FILE_PREFIX_PET}N"
                                         f"{len(aligned_PET_images)}.nii.gz")
        image_processing.average_images(aligned_PET_images, average_PET_image)
        iteration_PET_template = average_PET_image
        aligned_PET_images.clear()

        print(f'[OCELOT] Averaging SUV PET images.')
        average_SUV_PET_image = os.path.join(template_generation_directory,
                                             f"{alignment_iteration}_deformed_average_cohort_{c.FILE_PREFIX_SUV_PET}N"
                                             f"{len(aligned_SUV_PET_images)}.nii.gz")
        mean_SUV_PET = image_processing.average_images(aligned_SUV_PET_images, average_SUV_PET_image)
        iteration_SUV_PET_template = average_SUV_PET_image

        print(f'[OCELOT] Computing STD SUV PET images.')
        std_SUV_PET_image = os.path.join(template_generation_directory,
                                         f"{alignment_iteration}_deformed_average_cohort_STD_{c.FILE_PREFIX_SUV_PET}N"
                                         f"{len(aligned_SUV_PET_images)}.nii.gz")
        image_analysis.std_images(aligned_SUV_PET_images, mean_SUV_PET, std_SUV_PET_image)
        iteration_STD_SUV_PET_template = std_SUV_PET_image
        aligned_SUV_PET_images.clear()

        print(f"")

    print(f'[OCELOT] Template creation took {system.get_processing_time(total_time_start, "m")}.')

    # ------------------------------------------- NormDB folder creation --------------------------------------------- #
    print(f'\n[OCELOT] Storing normative template images in:')
    database_directory = os.path.join(ocelot_directory, f'NormDB_'
                                                        f'N{number_of_subjects}-subjects_'
                                                        f'N{alignment_iteration}-iterations_'
                                                        f'{cohort_name}')
    file_management.create_directory(database_directory)
    print(f'[OCELOT] {database_directory}')

    database_CT_path = os.path.join(database_directory, f"{c.FILE_PREFIX_CT}template_{cohort_name}.nii.gz")
    file_management.copy_file(iteration_CT_template, database_CT_path)

    database_PET_path = os.path.join(database_directory, f"{c.FILE_PREFIX_PET}template_{cohort_name}.nii.gz")
    file_management.copy_file(iteration_PET_template, database_PET_path)

    database_SUV_PET_path = os.path.join(database_directory, f"{c.FILE_PREFIX_SUV_PET}template_{cohort_name}.nii.gz")
    file_management.copy_file(iteration_SUV_PET_template, database_SUV_PET_path)

    database_STD_SUV_PET_path = os.path.join(database_directory, f"{c.FILE_PREFIX_STD_SUV_PET}template_{cohort_name}.nii.gz")
    file_management.copy_file(iteration_STD_SUV_PET_template, database_STD_SUV_PET_path)

    print(f'[OCELOT] Creating segmentations:')
    segmentation_interface.generate_all_required_segmentations(database_directory)

    if clean_up:
        print(f'[OCELOT] Removing {template_generation_directory} working directory from {ocelot_directory}.')
        file_management.delete_directory(template_generation_directory)
