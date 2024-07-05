# ------------------------------------------------------ Imports ----------------------------------------------------- #
import os
import shutil
import natsort
import pydicom

from ocelotz import constants


def get_filename(file_path: str) -> str:
    if os.path.isfile(file_path):
        file_name = os.path.basename(file_path)
        return file_name
    else:
        print("Not a file!")


def get_file_stem(file_path: str) -> str:
    file_basename = get_filename(file_path)
    file_stem = file_basename[:file_basename.find('.')]
    return file_stem


def get_file_extension(file_path: str) -> str:
    file_basename = get_filename(file_path)
    file_extension = file_basename[file_basename.find('.') + 1:]
    return file_extension


def copy_file(source_file_path: str, target_path: str) -> str:
    """
    Copies a source file to the specified destination
    @rtype: str
    @param source_file_path: the absolute path and file to copy
    @param target_path: the destination where the file will be copied to
    @return: a string containing the absolute path to the just copied file
    """
    if os.path.isfile(source_file_path):
        print(f'[Files]     Copying {source_file_path} to {target_path}')
        file_path = shutil.copy(source_file_path, target_path)
        return file_path
    else:
        print(f'[Files]     Error: {source_file_path} is not a file!')


def copy_directory(source_directory_path: str, target_directory_path: str) -> str:
    """
    Copies a source folder with its contents to the specified destination
    @rtype: str
    @param source_directory_path: the absolute path and folder to copy
    @param target_directory_path: the destination where the folder will be copied to
    @return: a string containing the absolute path to the just copied folder
    """
    if os.path.isdir(source_directory_path):
        source_folder_name = os.path.basename(source_directory_path)
        print(f'[Files]     Copying {source_folder_name} at {source_directory_path} to {target_directory_path}')
        directory_path = shutil.copytree(source_directory_path, target_directory_path)
        return directory_path
    else:
        print(f'[Files]     Error: {source_directory_path} is not a folder!')


def create_directory(directory_path: str) -> None:
    """
    Creates a directory
    @rtype: None
    @param directory_path: The directory to create
    """
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)


def delete_directory(directory_path: str) -> None:
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        shutil.rmtree(directory_path)


def get_files(directory_path) -> list[str]:
    items = os.listdir(directory_path)
    files = [item for item in items if os.path.isfile(os.path.join(directory_path, item)) and not item.startswith('.')]
    files = natsort.natsorted(files)
    return files


def get_files_with_suffix(directory_path, suffixes) -> list[str]:
    files = get_files(directory_path)
    if isinstance(suffixes, str):
        suffixes = [suffixes]
    files_with_suffix = [file for file in files if any(file.endswith(suffix) for suffix in suffixes)]
    return files_with_suffix


def get_DICOM_files(directory_path) -> list[str]:
    DICOM_SUFFIXES = ['.dcm', '.DCM', '.ima', '.IMA']
    dicom_files = get_files_with_suffix(directory_path, DICOM_SUFFIXES)
    return dicom_files


def get_NIFTI_files(directory_path) -> list[str]:
    NIFTI_SUFFIXES = ['.nii.gz', '.nii']
    dicom_files = get_files_with_suffix(directory_path, NIFTI_SUFFIXES)
    return dicom_files


def get_folders(directory_path) -> list[str]:
    items = os.listdir(directory_path)
    folders = [item for item in items if os.path.isdir(os.path.join(directory_path, item)) and not item.startswith('.')]
    folders = natsort.natsorted(folders)
    return folders


def get_subdirectories(directory_path) -> list[str]:
    folders = get_folders(directory_path)
    subdirectories = [os.path.join(directory_path, folder) for folder in folders]
    return subdirectories


def get_DICOM_folders(search_directory: str) -> list:
    DICOM_directories = []
    for root, directories, files in os.walk(search_directory):
        dicom_files = [file for file in files if file.lower().endswith(('.ima', '.dcm'))]
        if dicom_files:
            DICOM_directories.append(root)
    print(f"Found {len(DICOM_directories)} DICOM folders in {os.path.basename(search_directory)}.")
    return DICOM_directories


def get_modality_directory(DICOM_directories: list, modality: str) -> str | None:
    modality_directory = None
    for DICOM_directory in DICOM_directories:
        DICOM_files = os.listdir(DICOM_directory)
        DICOM_probe = pydicom.dcmread(os.path.join(DICOM_directory, DICOM_files[0]))
        if DICOM_probe.Modality == modality:
            modality_directory = DICOM_directory

    return modality_directory


def get_PET_directory(DICOM_directories: list) -> str:
    PET_directory = get_modality_directory(DICOM_directories, constants.DICOM_MODALITY_PET)
    return PET_directory


def get_CT_directory(DICOM_directories: list) -> str:
    CT_directory = get_modality_directory(DICOM_directories, constants.DICOM_MODALITY_CT)
    return CT_directory


def clear_directory(directory) -> None:
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


def file_exists(file_path: str) -> bool:
    exists = False
    if os.path.isfile(file_path):
        exists = os.path.exists(file_path)
    return exists


def get_image_path(subject_directory: str, prefix: str) -> str | None:
    nifti_files = get_NIFTI_files(subject_directory)
    for nifti_file in nifti_files:
        if nifti_file.startswith(prefix):
            return os.path.join(subject_directory, nifti_file)
    return None


def get_image_path_hierarchical(subject_directory: str, possible_prefixes: list) -> str | None:
    for prefix in possible_prefixes:
        image_path = get_image_path(subject_directory, prefix)
        if image_path is not None:
            return image_path
