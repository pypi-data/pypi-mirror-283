# ------------------------------------------------------ Imports ----------------------------------------------------- #
import os
import SimpleITK

from moosez.constants import ORGAN_INDICES
from moosez.resources import check_device
from moosez import moose

from ocelotz import image_processing
from ocelotz import file_management
from ocelotz import constants


CLIN_CT_BODY_MASK_INDICES = {}
CLIN_CT_ORGAN_INDICES = {}
REQUIRED_SEGMENTATIONS = []

for model, labels in ORGAN_INDICES.items():
    if model == 'clin_ct_body':
        CLIN_CT_BODY_MASK_INDICES[model] = labels
    elif model.startswith('clin_ct') and model not in constants.MODELS_TO_EXCLUDE:
        CLIN_CT_ORGAN_INDICES[model] = labels
        REQUIRED_SEGMENTATIONS.append(f"{constants.FILE_PREFIX_LABEL}{model}.nii.gz")
REQUIRED_SEGMENTATIONS.append(constants.RESIDUAL_BODY_MASK_NAME)


def generate_segmentation(subject_directory: str, model_label_indices: dict):
    print(f"[OCELOT]    Detecting missing segmentations.")
    missing_segmentations = determine_missing_segmentations(subject_directory, model_label_indices)
    if len(missing_segmentations) == 0:
        print(f"[OCELOT]       All required segmentations exist.")
        return

    accelerator = check_device()

    output_directory = os.path.join(subject_directory, 'temp_output')
    file_management.create_directory(output_directory)

    input_directory = os.path.join(subject_directory, 'temp_input')
    file_management.create_directory(input_directory)

    CT_prefixes = [constants.FILE_PREFIX_CT_PET_ALIGNED, constants.FILE_PREFIX_CT]
    CT_image_path = file_management.get_image_path_hierarchical(subject_directory, CT_prefixes)
    if CT_image_path is None:
        raise FileNotFoundError("No valid CT image was found!")
    file_management.copy_file(CT_image_path, input_directory)

    for model in missing_segmentations:
        segmentation_file_name = f'{constants.FILE_PREFIX_LABEL}{model}.nii.gz'
        print(f"[OCELOT]    Predicting: {model}")
        moose(model, input_directory, output_directory, accelerator)
        moose_image_path = file_management.get_image_path(output_directory, constants.FILE_PREFIX_CT)
        segmentation_image_path = os.path.join(subject_directory, segmentation_file_name)
        file_management.copy_file(moose_image_path, segmentation_image_path)
        file_management.clear_directory(output_directory)

    file_management.delete_directory(input_directory)
    file_management.delete_directory(output_directory)


def determine_missing_segmentations(subject_directory: str, model_label_indices: dict) -> list:
    missing_segmentations = []
    for model in model_label_indices.keys():
        segmentation_file_name = f'{constants.FILE_PREFIX_LABEL}{model}.nii.gz'
        segmentation_file_path = os.path.join(subject_directory, segmentation_file_name)
        if file_management.file_exists(segmentation_file_path):
            print(f"[OCELOT]       {model} segmentation already exists.")
        else:
            missing_segmentations.append(model)
    return missing_segmentations


def generate_residual_mask(subject_directory: str):
    print(f"[OCELOT]    Detecting residual body mask.")
    residual_body_mask_path = os.path.join(subject_directory, constants.RESIDUAL_BODY_MASK_NAME)
    if file_management.file_exists(residual_body_mask_path):
        print(f"[OCELOT]       Residual body mask already exists.")
        return

    body_mask_name = f"{constants.FILE_PREFIX_LABEL}clin_ct_body.nii.gz"
    body_mask_path = os.path.join(subject_directory, body_mask_name)

    whole_body_mask_image = image_processing.binarize_mask(body_mask_path)
    SimpleITK.WriteImage(whole_body_mask_image, os.path.join(subject_directory, constants.WHOLE_BODY_MASK_NAME))

    label_file_names = [label_file_name for label_file_name in os.listdir(subject_directory) if
                        label_file_name.startswith(constants.FILE_PREFIX_LABEL) and
                        (label_file_name.endswith('.nii.gz') or label_file_name.endswith('.nii')) and
                        "body" not in label_file_name and "residual" not in label_file_name]

    residual_body_mask = whole_body_mask_image
    for label_file_name in label_file_names:
        print(f"[OCELOT]    Removing {label_file_name} regions from {body_mask_name}")
        label_file_path = os.path.join(subject_directory, label_file_name)

        binarized_label_image = image_processing.binarize_mask(label_file_path)
        masked_binarized_label_image = SimpleITK.Mask(binarized_label_image, whole_body_mask_image)
        inverted_binarized_label_image = 1 - masked_binarized_label_image
        residual_body_mask = residual_body_mask * inverted_binarized_label_image

    SimpleITK.WriteImage(residual_body_mask, os.path.join(subject_directory, constants.RESIDUAL_BODY_MASK_NAME))


def mask_regions(subject_directory: str, regions_to_mask: list, output_directory: str = None) -> str:
    if regions_to_mask is None:
        return subject_directory

    if output_directory is None:
        masked_labels_directory = os.path.join(subject_directory, f'{constants.FILE_PREFIX_LABEL}masked')
        file_management.create_directory(masked_labels_directory)
    else:
        masked_labels_directory = output_directory

    regions_to_mask = [region_to_mask.lower() for region_to_mask in regions_to_mask]
    label_file_names = [label_file_name for label_file_name in os.listdir(subject_directory) if
                        label_file_name.startswith(constants.FILE_PREFIX_LABEL) and
                        (label_file_name.endswith('.nii.gz') or label_file_name.endswith('.nii'))]

    indices_to_keep = []
    for available_index_to_mask, available_region_to_mask in ORGAN_INDICES["clin_ct_body"].items():
        if available_region_to_mask.lower() not in regions_to_mask:
            indices_to_keep.append(available_index_to_mask)
    if len(indices_to_keep) == 0:
        print("Can not mask all regions.")
        return subject_directory

    full_body_mask_path = os.path.join(subject_directory, f"{constants.FILE_PREFIX_LABEL}clin_ct_body.nii.gz")
    masking_body_mask_path = os.path.join(masked_labels_directory, f"{constants.MASKING_BODY_MASK_NAME}")
    image_processing.binarize_mask(full_body_mask_path, indices_to_keep, masking_body_mask_path)

    for label_file_name in label_file_names:
        print(f"[OCELOT]    Removing {', '.join(regions_to_mask)} from {label_file_name}")
        label_file_path = os.path.join(subject_directory, label_file_name)
        masked_label_file_path = os.path.join(masked_labels_directory, label_file_name)
        image_processing.mask_image(label_file_path, masking_body_mask_path, masked_label_file_path)

    return masked_labels_directory


def generate_all_required_segmentations(subject_directory: str) -> None:
    generate_segmentation(subject_directory, CLIN_CT_ORGAN_INDICES)
    generate_segmentation(subject_directory, CLIN_CT_BODY_MASK_INDICES)
    generate_residual_mask(subject_directory)


def regions_string_to_list(regions_to_mask_string: str) -> list | None:
    if regions_to_mask_string is None:
        return None
    regions = regions_to_mask_string.split(',')
    if len(regions) == 0:
        raise ValueError(f"Error in retrieving regions from string: {regions_to_mask_string}")
    allowed_regions = [allowed_region.lower() for allowed_region in ORGAN_INDICES["clin_ct_body"].values()]
    regions_to_mask_list = [region for region in regions if region in allowed_regions]
    if len(regions_to_mask_list) == 0:
        return None
    return regions_to_mask_list


def body_mask_image(image_path: str, masked_image_path: str = None) -> SimpleITK.Image:
    image_directory = os.path.dirname(image_path)
    generate_segmentation(image_directory, CLIN_CT_BODY_MASK_INDICES)
    body_mask_name = f"{constants.FILE_PREFIX_LABEL}{constants.FILE_PREFIX_MODEL_CLINICAL_CT}body.nii.gz"
    body_mask_path = os.path.join(image_directory, body_mask_name)

    whole_body_mask_image = image_processing.binarize_mask(body_mask_path)
    image_to_mask = SimpleITK.ReadImage(image_path)
    masked_image = SimpleITK.Mask(image_to_mask, whole_body_mask_image, constants.CT_BACKGROUND_VALUE)

    if masked_image_path is not None:
        SimpleITK.WriteImage(masked_image, masked_image_path)

    return masked_image
