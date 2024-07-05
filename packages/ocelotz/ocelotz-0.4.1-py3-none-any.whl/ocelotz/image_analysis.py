# ------------------------------------------------------ Imports ----------------------------------------------------- #
import os
import SimpleITK
import numpy as np
from tqdm import tqdm

from ocelotz import image_processing


def std_images(image_stack: list, mean_image: SimpleITK.Image = None, std_image_path: str = None) -> SimpleITK.Image:

    if mean_image is None:
        mean_image = image_processing.average_images(image_stack)

    diff_image = SimpleITK.ReadImage(image_stack[0], SimpleITK.sitkFloat64) - mean_image
    squared_diff_image = diff_image ** 2
    summed_image_std = squared_diff_image

    # Process all other images
    for image_index in (pbar := tqdm(range(1, len(image_stack)))):
        pbar.set_description(f"[OCELOT] Adding the difference image of {os.path.basename(image_stack[image_index])} "
                             f"to the original image ({os.path.basename(image_stack[0])}).")
        diff_image = SimpleITK.ReadImage(image_stack[image_index], SimpleITK.sitkFloat64) - mean_image
        squared_diff_image = diff_image ** 2
        summed_image_std = summed_image_std + squared_diff_image
    number_of_images = len(image_stack)
    std_image = pow(summed_image_std * (1 / number_of_images), 1 / 2)

    if std_image_path is not None:
        SimpleITK.WriteImage(std_image, std_image_path)

    return std_image


def compute_z_map(sample: SimpleITK.Image, mean: SimpleITK.Image, std: SimpleITK.Image) -> SimpleITK.Image:
    print(f'[OCELOT]   Computing z-map')

    # The diff image is computed as SimpleITK.Image
    diff_image = sample - mean

    # The needed images for division as numpy arrays:
    diff_image_np = SimpleITK.GetArrayFromImage(diff_image)
    std_image_np = SimpleITK.GetArrayFromImage(std)

    # Division only at voxels higher than 0.01
    z_map_np = np.divide(diff_image_np, std_image_np, where=(std_image_np >= 0.01))

    # Create a SimpleITK image from the numpy z-map
    z_map = SimpleITK.GetImageFromArray(z_map_np)
    z_map.SetOrigin(diff_image.GetOrigin())
    z_map.SetSpacing(diff_image.GetSpacing())
    z_map.SetDirection(diff_image.GetDirection())

    return z_map


def compute_percentage_difference_map(sample: SimpleITK.Image, mean: SimpleITK.Image) -> SimpleITK.Image:
    print(f'[OCELOT]   Computing percentage-difference-map')

    diff_image = sample - mean

    # The needed images for division as numpy arrays:
    diff_image_np = SimpleITK.GetArrayFromImage(diff_image)
    mean_image_np = SimpleITK.GetArrayFromImage(mean)

    # Division only at voxels higher than 0.01
    percentage_difference_map_np = (np.divide(diff_image_np, mean_image_np, where=(mean_image_np >= 0.01)))*100

    # Create a SimpleITK image from the numpy z-map
    percentage_difference_map = SimpleITK.GetImageFromArray(percentage_difference_map_np)
    percentage_difference_map.SetOrigin(diff_image.GetOrigin())
    percentage_difference_map.SetSpacing(diff_image.GetSpacing())
    percentage_difference_map.SetDirection(diff_image.GetDirection())

    return percentage_difference_map


def compute_euclidean_distance(p: tuple, q: tuple) -> float:
    """
    Computes the Euclidean distance between point q and p
    @param p: Point q as tuple
    @param q: Point p as tuple
    @return: The Euclidean distance between p and q
    @rtype: float
    """
    if len(p) == len(q):
        euclidean_distance = np.linalg.norm(np.subtract(p, q))
    else:
        euclidean_distance = -1
        print('ERROR: the two points do not share the same number of coordinates.')
    return euclidean_distance


def get_closest_label_pairs(reference_label_image_path: str, label_image_path: str) -> list:
    """
    Creates a list with label pairs which are the closest to each other based on Euclidean distance
    @param reference_label_image_path: A path to an image containing labels
    @param label_image_path: A path to an image containing labels
    @return: List of the closest label pairs
    @rtype: list
    """
    reference_label_image = SimpleITK.ReadImage(reference_label_image_path, SimpleITK.sitkInt8)
    label_image = SimpleITK.ReadImage(label_image_path, SimpleITK.sitkInt8)

    if not image_processing.image_geometries_identical(reference_label_image, label_image):
        resliced_label_image = image_processing.reslice_identity(reference_label_image, label_image, is_label_image=True)
    else:
        resliced_label_image = label_image

    stats_reference_label_image = SimpleITK.LabelShapeStatisticsImageFilter()
    stats_reference_label_image.Execute(SimpleITK.ConnectedComponent(reference_label_image))

    stats_resliced_label_image = SimpleITK.LabelShapeStatisticsImageFilter()
    stats_resliced_label_image.Execute(SimpleITK.ConnectedComponent(resliced_label_image))

    closest_label_pairs = []
    number_of_labels = 0
    if len(stats_reference_label_image.GetLabels()) == len(stats_resliced_label_image.GetLabels()):
        number_of_labels = len(stats_reference_label_image.GetLabels())

    if number_of_labels != 2:
        return closest_label_pairs

    for i1 in range(1, number_of_labels + 1):
        smallest_euclidean_distance = float('inf')
        label_pair = (0, 0, smallest_euclidean_distance)
        for i2 in range(1, number_of_labels + 1):

            euclidean_distance = compute_euclidean_distance(stats_reference_label_image.GetCentroid(i1),
                                                            stats_resliced_label_image.GetCentroid(i2))
            if euclidean_distance < smallest_euclidean_distance:
                smallest_euclidean_distance = euclidean_distance
                label_pair = (i1, i2, smallest_euclidean_distance)

        # print(f'{label_pair[0]} | {label_pair[1]} identified with smallest found distance of: {label_pair[2]}')
        closest_label_pairs.append(label_pair)

    return closest_label_pairs


def get_label_mean_intensity_metrics(intensity_image: SimpleITK.Image, label_image: SimpleITK.Image, selected_label: int = None) -> float | dict | None:
    intensity_stats = SimpleITK.LabelIntensityStatisticsImageFilter()
    intensity_stats.Execute(label_image, intensity_image)

    if selected_label is not None:
        return round(intensity_stats.GetMean(selected_label), 2)

    if intensity_stats.GetNumberOfLabels() == 1:
        existing_label = intensity_stats.GetLabels()[0]
        return round(intensity_stats.GetMean(existing_label), 2)

    means = {}
    for existing_label in intensity_stats.GetLabels():
        means[existing_label] = round(intensity_stats.GetMean(existing_label), 2)
    if len(means) == 0:
        return None
    return means


def get_label_volume_metrics(label_image: SimpleITK, selected_label: int = None) -> float | list | None:
    label_shape_statistics_filter = SimpleITK.LabelShapeStatisticsImageFilter()
    label_shape_statistics_filter.Execute(label_image)

    if selected_label is not None:
        return round(label_shape_statistics_filter.GetPhysicalSize(selected_label), 2)

    if label_shape_statistics_filter.GetNumberOfLabels() == 1:
        existing_label = label_shape_statistics_filter.GetLabels()[0]
        return round(label_shape_statistics_filter.GetPhysicalSize(existing_label), 2)

    volumes = []
    for existing_label in label_shape_statistics_filter.GetLabels():
        volumes.append(round(label_shape_statistics_filter.GetPhysicalSize(existing_label), 2))
    if len(volumes) == 0:
        return None
    return volumes
