# ------------------------------------------------------ Imports ----------------------------------------------------- #
import pyfiglet
import emoji

from ocelotz import constants
from ocelotz import system


def logo():
    """
    Display OCELOT logo
    :return:
    """
    print(" ")
    print(constants.ANSI_VIOLET + pyfiglet.figlet_format(f"OCELOT {constants.OCELOT_VERSION}", font="smslant").rstrip() + "\033[0m")
    print(constants.ANSI_VIOLET + "A part of the ENHANCE community. Join us at www.enhance.pet to build the future of PET imaging together." + "\033[0m")
    print(" ")


def citation():
    """
    Display manuscript citation
    :return:
    """
    print(f'{constants.ANSI_VIOLET}{emoji.emojize(":scroll:")} CITATION:{constants.ANSI_RESET}')
    print(" ")
    print("Gutschmayer S, Muzik O, Shiyam Sundar LK et al. "
          "OCELOT: DiffeOmorphiC rEgistration for voxel-wise anOmaly Tracking - a tool to generate cohort specific normative PET/CT images. To be submitted at Journal Nuclear Med. 2024.")
    print("Copyright 2024, Quantitative Imaging and Medical Physics Team, Medical University of Vienna")
    print(" ")


def usage():
    print(f'{constants.ANSI_VIOLET}{emoji.emojize(":scroll:")} USAGE:{constants.ANSI_RESET}')
    print(" ")
    print(f"Please use one of the following argument configurations for OCELOT to:")
    print(f"- create a template image from a cohort:"
          f"\n   ocelot normalize -sub-dir <path/to/cohort/directory>")
    print(f"- stratify subject folders:"
          f"\n   ocelot stratify -dir <path/to/unstratified/subject/directory>")
    print(f"- compare a subject to the template image:"
          f"\n   ocelot compare -ref-dir <path/to/normdb/directory> -sub-dir <path/to/patients/directory>")
    print(" ")


def template_image_creation(stratified_subjects_directory):
    print(f'{constants.ANSI_VIOLET}{emoji.emojize(":x-ray:")} TEMPLATE IMAGE CREATION:{constants.ANSI_RESET}')
    print(" ")
    print(f"[OCELOT] Cohort directory: {stratified_subjects_directory}")
    print(" ")


def subject_stratification(unstratified_subjects_directory, stratified_subjects_directory):
    print(f'{constants.ANSI_VIOLET}{emoji.emojize(":card_index_dividers:")} SUBJECT STRATIFICATION:{constants.ANSI_RESET}')
    print(" ")
    print(f"[OCELOT] Subject directory: {unstratified_subjects_directory}")
    print(f"[OCELOT] Cohort directory:  {stratified_subjects_directory}")
    print(" ")


def patient_comparison(patients_directory, normative_database_directory):
    print(f'{constants.ANSI_VIOLET}{emoji.emojize(":magnifying_glass_tilted_right:")} DETECTING ABERRATIONS:{constants.ANSI_RESET}')
    print(" ")
    print(f"[OCELOT] Patient directory:            {patients_directory}")
    print(f"[OCELOT] Normative database directory: {normative_database_directory}")
    print(" ")


def download():
    print(f'{constants.ANSI_VIOLET}{emoji.emojize(":globe_with_meridians:")} BINARIES DOWNLOAD:{constants.ANSI_RESET}')
    print('')


def system_information():
    operating_system = system.get_operating_system()
    architecture = system.get_architecture()

    print(f'{constants.ANSI_ORANGE}Detected system: {operating_system} | Detected architecture: {architecture}'
          f'{constants.ANSI_RESET}')
    print('')
