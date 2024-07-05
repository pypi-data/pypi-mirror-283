# ------------------------------------------------------ Imports ----------------------------------------------------- #
import SimpleITK
import os
import numpy
from tqdm import tqdm

from ocelotz import file_management


def scale_image(image_path: str, scale_factor: float, scaled_image_path: str = None) -> SimpleITK.Image:
    image = SimpleITK.ReadImage(image_path, SimpleITK.sitkFloat64)
    scaled_image = image * scale_factor

    if scaled_image_path is not None:
        SimpleITK.WriteImage(scaled_image, scaled_image_path)

    return scaled_image


def sum_images(image_stack: list, summed_image_path: str = None) -> SimpleITK.Image:
    # Start with the first image
    summed_image = SimpleITK.ReadImage(image_stack[0], SimpleITK.sitkFloat64)

    # Sum all other images
    for image_index in (pbar := tqdm(range(1, len(image_stack)))):
        pbar.set_description(f"[OCELOT] Adding {os.path.basename(image_stack[image_index])} to the original image ({os.path.basename(image_stack[0])}).")
        current_image = SimpleITK.ReadImage(image_stack[image_index], SimpleITK.sitkFloat64)
        summed_image = summed_image + current_image

    if summed_image_path is not None:
        SimpleITK.WriteImage(summed_image, summed_image_path)

    return summed_image


def average_images(image_stack: list, averaged_image_path: str = None) -> SimpleITK.Image:
    summed_image = sum_images(image_stack)

    number_of_images = len(image_stack)
    print(f"[OCELOT] Averaging {number_of_images} images.")
    averaged_image = summed_image / number_of_images

    if averaged_image_path is not None:
        SimpleITK.WriteImage(averaged_image, averaged_image_path)

    return averaged_image


def keep_largest_label(input_image, output_image=None):
    binary_image = SimpleITK.ReadImage(input_image, SimpleITK.sitkInt8)
    component_image = SimpleITK.ConnectedComponent(binary_image)
    sorted_component_image = SimpleITK.RelabelComponent(component_image, sortByObjectSize=True)
    largest_component_binary_image = sorted_component_image == 1

    if output_image is None:
        SimpleITK.WriteImage(largest_component_binary_image, input_image)
    else:
        SimpleITK.WriteImage(largest_component_binary_image, output_image)


def extract_label(label_image: SimpleITK.Image, label_index: int, output_image_path: str = None) -> SimpleITK.Image:
    extracted_label_image = (label_image == label_index) * label_index

    if output_image_path is not None:
        SimpleITK.WriteImage(extracted_label_image, output_image_path)

    return extracted_label_image


def is_empty_segmentation(label_image: SimpleITK.Image, threshold: int = 10) -> bool:
    label_image_array = SimpleITK.GetArrayFromImage(label_image)
    if numpy.count_nonzero(label_image_array) <= threshold:
        return True
    else:
        return False


def image_geometries_identical(image_1: SimpleITK.Image, image_2: SimpleITK.Image) -> bool:
    """
    Checks if the image geometries are identical
    :param image_1: the first image to be compared
    :param image_2: the second image to be compared
    :return: bool
    """
    return (image_1.GetSize() == image_2.GetSize() and
            image_1.GetSpacing() == image_2.GetSpacing() and
            image_1.GetOrigin() == image_2.GetOrigin())


def cast_image_pixel_type(reference_image: SimpleITK.Image, image: SimpleITK.Image) -> SimpleITK.Image:
    """
    Casts the image pixel type to the reference image pixel type
    :param reference_image: the reference image to get the desired pixel type
    :param image: the image to cast to the reference pixel type
    :return: SimpleITK.Image
    """
    reference_pixel_type = reference_image.GetPixelIDValue()
    image_pixel_type = image.GetPixelIDValue()
    if image_pixel_type != reference_pixel_type:
        return SimpleITK.Cast(image, reference_pixel_type)
    else:
        return image


def reslice_transform(reference_image: SimpleITK.Image, image: SimpleITK.Image, transform: SimpleITK.Transform,
                      output_image_path: str = None, is_label_image: bool = False) -> SimpleITK.Image:
    """
    Re-slices an image to the same space as another image by any transform.
    :param reference_image: The reference image
    :param image: The image to reslice
    :param transform: The SimpleITK.Transform to apply to the image
    :param output_image_path: Path to the resliced image
    :param is_label_image: Determines if the image is a label image. Default is False
    :return: SimpleITK.Image
    """

    image = cast_image_pixel_type(reference_image, image)

    if is_label_image:
        interpolator = SimpleITK.sitkNearestNeighbor
    else:
        interpolator = SimpleITK.sitkLinear

    resampled_image = SimpleITK.Resample(image, reference_image, transform, interpolator)

    if output_image_path is not None:
        SimpleITK.WriteImage(resampled_image, output_image_path)
    return resampled_image


def reslice_center(reference_image: SimpleITK.Image, image: SimpleITK.Image,
                   output_image_path: str = None, is_label_image: bool = False) -> SimpleITK.Image:
    """
    Re-slices an image to the same space as another image by a center transform.
    :param reference_image: The reference image
    :param image: The image to reslice
    :param output_image_path: Path to the resliced image
    :param is_label_image: Determines if the image is a label image. Default is False
    :return: SimpleITK.Image
    """

    center_transform = SimpleITK.CenteredTransformInitializer(reference_image, image, SimpleITK.Euler3DTransform(),
                                                              SimpleITK.CenteredTransformInitializerFilter.GEOMETRY)
    resampled_image = reslice_transform(reference_image, image, center_transform, output_image_path, is_label_image)
    return resampled_image


def reslice_identity(reference_image: SimpleITK.Image, image: SimpleITK.Image,
                     output_image_path: str = None, is_label_image: bool = False) -> SimpleITK.Image:
    """
    Re-slices an image to the same space as another image by an identity transform.
    :param reference_image: The reference image
    :param image: The image to reslice
    :param output_image_path: Path to the resliced image
    :param is_label_image: Determines if the image is a label image. Default is False
    :return: SimpleITK.Image
    """

    identity_transform = SimpleITK.Transform(reference_image.GetDimension(), SimpleITK.sitkIdentity)
    resampled_image = reslice_transform(reference_image, image, identity_transform, output_image_path, is_label_image)
    return resampled_image


def split_labels(reference_label_image_path: str, label_image_path: str, closest_label_pairs: list) -> list:
    if not closest_label_pairs:
        return [(reference_label_image_path, label_image_path)]

    reference_label_image = SimpleITK.ReadImage(reference_label_image_path, SimpleITK.sitkInt8)
    label_image = SimpleITK.ReadImage(label_image_path, SimpleITK.sitkInt8)

    # Extract the statistics
    cc_reference_label_image = SimpleITK.ConnectedComponent(reference_label_image)
    cc_label_image = SimpleITK.ConnectedComponent(label_image)

    extracted_label_pairs = []
    for label_pair in closest_label_pairs:
        output_reference_file_path = os.path.join(os.path.dirname(reference_label_image_path),
                                                  f'{file_management.get_file_stem(reference_label_image_path)}_'
                                                  f'{label_pair[0]}.'
                                                  f'{file_management.get_file_extension(reference_label_image_path)}')
        extract_label(cc_reference_label_image, label_pair[0], output_reference_file_path)
        output_file_path = os.path.join(os.path.dirname(label_image_path),
                                        f'{file_management.get_file_stem(label_image_path)}_'
                                        f'{label_pair[1]}.'
                                        f'{file_management.get_file_extension(label_image_path)}')
        extract_label(cc_label_image, label_pair[1], output_file_path)
        extracted_label_pairs.append((output_reference_file_path, output_file_path))

    return extracted_label_pairs


def mask_image(image_path: str, mask_path: str, masked_image_path=None) -> SimpleITK.Image:
    image = SimpleITK.ReadImage(image_path)
    mask = SimpleITK.ReadImage(mask_path, SimpleITK.sitkUInt8)
    masked_image = SimpleITK.Mask(image, mask)

    if masked_image_path is not None:
        SimpleITK.WriteImage(masked_image, masked_image_path)

    return masked_image


def binarize_mask(mask_path: str, labels_to_keep=None, binarized_mask_path=None) -> SimpleITK.Image:
    mask = SimpleITK.ReadImage(mask_path, SimpleITK.sitkUInt8)

    if labels_to_keep is None:
        binarized_mask = mask > 0

    else:
        binarized_mask = SimpleITK.Image(mask.GetSize(), SimpleITK.sitkUInt8)
        binarized_mask.CopyInformation(mask)
        for label in labels_to_keep:
            label_mask = mask == label
            binarized_mask = binarized_mask + label_mask

    if binarized_mask_path is not None:
        SimpleITK.WriteImage(binarized_mask, binarized_mask_path)

    return binarized_mask


def erode_mask(mask_path: str, labels_to_erode=None, eroded_mask_path=None) -> SimpleITK.Image:
    mask_image = SimpleITK.ReadImage(mask_path, SimpleITK.sitkUInt8)

    if labels_to_erode is None:
        labels_to_erode = [1]

    for label_to_erode in labels_to_erode:
        mask_image = SimpleITK.BinaryErode(mask_image, (1, 1, 1), SimpleITK.sitkBox, 0, label_to_erode)

    if eroded_mask_path is not None:
        SimpleITK.WriteImage(mask_image, eroded_mask_path)

    return mask_image
