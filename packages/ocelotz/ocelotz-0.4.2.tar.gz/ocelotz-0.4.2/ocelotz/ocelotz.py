#!/usr/bin/env python3

# ---------------------------------------------------- Description --------------------------------------------------- #
# OCELOT v0.4.0
# -------------------------------------------------------------------------------------------------------------------- #
#
# Sebastian Gutschmayer
# Medical University of Vienna
# Quantitative Imaging and Medical Physics (QIMP) Team
# -------------------------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------ Imports ----------------------------------------------------- #
import argparse

from ocelotz import subject_stratification
from ocelotz import subject_comparison
from ocelotz import subject_normalization
from ocelotz import display
from ocelotz import download


# ---------------------------------------------------- Functions ----------------------------------------------------- #

# ------------------------------------------------- NormDB creation -------------------------------------------------- #
def normalize_command(args):
    subject_directory = args.subject_directory
    clean_up_working_directory = args.clean_up_working_directory
    display.template_image_creation(subject_directory)
    subject_normalization.create_template_images_EXPERIMENTAL(subject_directory, clean_up_working_directory)


# ------------------------------------------------ Patient comparison ------------------------------------------------ #
def compare_command(args):
    reference_directory = args.reference_directory
    subject_directory = args.subject_directory
    clean_up_working_directory = args.clean_up_working_directory
    mask_regions = args.mask_regions
    display.patient_comparison(subject_directory, reference_directory)
    subject_comparison.compare_subjects(reference_directory, subject_directory, clean_up_working_directory, mask_regions)


# -------------------------------------------------- Stratification -------------------------------------------------- #
def stratify_command(args):
    directory = args.directory
    display.subject_stratification(directory, directory)
    subject_stratification.stratify_and_standardize_subjects(directory, directory)


# ----------------------------------------------------- Default ------------------------------------------------------ #
def invalid_command():
    display.usage()
    exit(0)


# ------------------------------------------------------ Main -------------------------------------------------------- #
def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="Available Commands", dest="command")

    # Stratify command
    stratify_parser = subparsers.add_parser("stratify", help="Stratify subject data.")
    stratify_parser.add_argument("-dir", "--directory", required=True,
                                 help="Directory for subject stratification")

    # Normalize command
    normalize_parser = subparsers.add_parser("normalize", help="Normalize subject data.")
    normalize_parser.add_argument("-sub-dir", "--subject_directory", required=True,
                                  help="Directory for normalization")
    normalize_parser.add_argument("-clean-up", "--clean_up_working_directory", action='store_true',
                                  help="Optionally clean up working directory after processing.")

    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare patients to reference.")
    compare_parser.add_argument("-ref-dir", "--reference_directory", required=True,
                                help="Reference directory")
    compare_parser.add_argument("-sub-dir", "--subject_directory", required=True,
                                help="Subject directory")
    compare_parser.add_argument("-clean-up", "--clean_up_working_directory", action='store_true',
                                help="Optionally clean up working directory after processing.")
    compare_parser.add_argument("-mask-regions", "--mask_regions", default=None,
                                help="Optionally ignore specified regions: arms | legs | head.")

    args = parser.parse_args()

    # ------------------------------------------ Logo and citation display ------------------------------------------- #
    display.logo()
    display.citation()

    # --------------------------------------- Binary and system configuration ---------------------------------------- #
    display.download()
    display.system_information()
    download.binaries()

    # ----------------------------------------- Run OCELOT in selected mode ------------------------------------------ #
    if args.command == "stratify":
        stratify_command(args)
    elif args.command == "normalize":
        normalize_command(args)
    elif args.command == "compare":
        compare_command(args)
    else:
        invalid_command()

    # -------------------------------------------------- Exit OCELOT ------------------------------------------------- #
    print(f'\n[OCELOT] finished successfully.')
    exit(0)


# --------------------------------------------------- Main program --------------------------------------------------- #
if __name__ == '__main__':
    main()
