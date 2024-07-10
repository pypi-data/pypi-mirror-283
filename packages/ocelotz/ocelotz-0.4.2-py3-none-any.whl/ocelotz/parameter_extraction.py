# ------------------------------------------------------ Imports ----------------------------------------------------- #
import os
import SimpleITK
import pandas
from tqdm import tqdm

from ocelotz import subject_comparison
from ocelotz import file_management
from ocelotz import segmentation_interface
from ocelotz import image_processing
from ocelotz import image_analysis
from ocelotz import constants


def combine_dataframes_on_column(data_frames: list, column_name: str):
    if len(data_frames) == 0:
        return data_frames[0]
    combined_df = data_frames[0]
    for df in data_frames[1:]:
        combined_df = pandas.merge(combined_df, df, on=column_name, how='outer')
    return combined_df


def aggregate_volumes(subjects_directory: str):
    subject_label_volumes_dataframes = []

    subject_directories = file_management.get_subdirectories(subjects_directory)
    for subject_directory in subject_directories:
        subject_folder_name = os.path.basename(subject_directory)
        subject_label_volumes = []

        print(f"Creating segmentations for {subject_folder_name}.")
        segmentation_interface.generate_all_required_segmentations(subject_directory)

        print(f"Getting volumes for        {subject_folder_name}.")
        for TISSUE in (pbar := tqdm(subject_comparison.TISSUE_SEQUENCE)):
            tissue_mask_path = os.path.join(subject_directory, TISSUE.label_file_name)
            tissue_mask_image = SimpleITK.ReadImage(tissue_mask_path, SimpleITK.sitkUInt8)
            extracted_tissue_mask_image = image_processing.extract_label(tissue_mask_image, TISSUE.label_intensity)
            subject_label_volume = image_analysis.get_label_volume_metrics(extracted_tissue_mask_image)
            subject_label_volumes.append([TISSUE.name, subject_label_volume])
            pbar.set_description(f"{TISSUE.name:<{30}} volume: {subject_label_volume}.")

        subject_csv_file_path = os.path.join(subject_directory, f"{subject_folder_name}_volumes.csv")
        subject_label_volumes_dataframe = pandas.DataFrame(subject_label_volumes,
                                                           columns=[constants.LABEL_NAME_COLUMN_HEADER, f'{subject_folder_name} {constants.VOLUME_COLUMN_HEADER}'])
        print(f"Saving volume stats for    {subject_folder_name}.")
        subject_label_volumes_dataframe.to_csv(subject_csv_file_path, index=False)
        subject_label_volumes_dataframes.append(subject_label_volumes_dataframe)

    cohort_label_volumes_dataframe = combine_dataframes_on_column(subject_label_volumes_dataframes, constants.LABEL_NAME_COLUMN_HEADER)
    stats_csv_path = os.path.join(subjects_directory, "cohort_organ_volumes.csv")
    cohort_label_volumes_dataframe.to_csv(stats_csv_path)

    if len(subject_directories) > 1:
        print(f"Creating STD and Mean of cohort.")
        numeric_df = cohort_label_volumes_dataframe.select_dtypes(include=['number'])
        row_means = numeric_df.mean(axis=1)
        row_stds = numeric_df.std(axis=1)
        cohort_label_volumes_dataframe[f'Mean {constants.VOLUME_COLUMN_HEADER}'] = row_means
        cohort_label_volumes_dataframe[f'STD {constants.VOLUME_COLUMN_HEADER}'] = row_stds

        mean_and_std_csv_path = os.path.join(subjects_directory, "cohort_organ_volumes_mean+std.csv")
        cohort_label_volumes_dataframe.to_csv(mean_and_std_csv_path)
