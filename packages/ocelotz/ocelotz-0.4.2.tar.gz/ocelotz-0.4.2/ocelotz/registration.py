# ------------------------------------------------------ Imports ----------------------------------------------------- #
import subprocess

from ocelotz import constants as c
from ocelotz import system


def moments(reference_image_path: str, moving_image_path: str, moments_transform_path: str):
    command_string = f"{system.GREEDY_PATH} " \
                     f"-d 3 " \
                     f"-moments 1 " \
                     f"-i {reference_image_path} {moving_image_path} " \
                     f"-o {moments_transform_path}"
    subprocess.run(command_string, shell=True, capture_output=c.SILENT_CMD)


def rigid(reference_image_path: str, moving_image_path: str, transform_file_path: str, cost_function: str,
          initial_transform_path: str = None, resolution_scheme: str = c.MULTI_RESOLUTION_SCHEME):

    if initial_transform_path is None:
        initial_transform = f"-image-centers"
    else:
        initial_transform = f" {initial_transform_path}"

    command_string = f"{system.GREEDY_PATH} " \
                     f"-d 3 " \
                     f"-a " \
                     f"-dof 6 " \
                     f"-ia{initial_transform} " \
                     f"-i {reference_image_path} {moving_image_path} " \
                     f"-o {transform_file_path} " \
                     f"-n {resolution_scheme} " \
                     f"-m {cost_function}"
    subprocess.run(command_string, shell=True, capture_output=c.SILENT_CMD)


def affine(reference_image_path: str, moving_image_path: str, transform_file_path: str, cost_function: str,
           initial_transform_path: str = None, resolution_scheme: str = c.MULTI_RESOLUTION_SCHEME):

    if initial_transform_path is None:
        initial_transform = f"-image-centers"
    else:
        initial_transform = f" {initial_transform_path}"

    command_string = f"{system.GREEDY_PATH} " \
                     f"-d 3 " \
                     f"-a " \
                     f"-dof 12 " \
                     f"-ia{initial_transform} " \
                     f"-i {reference_image_path} {moving_image_path} " \
                     f"-o {transform_file_path} " \
                     f"-n {resolution_scheme} " \
                     f"-m {cost_function}"
    subprocess.run(command_string, shell=True, capture_output=c.SILENT_CMD)


def deformable(reference_image_path: str, moving_image_path: str, warp_file_path: str, cost_function: str,
               initial_transform_path: str = None, inverse_warp_file_path: str = None, resolution_scheme: str = c.MULTI_RESOLUTION_SCHEME):

    if initial_transform_path is None:
        initial_transform = f""
    else:
        initial_transform = f"-it {initial_transform_path} "

    if inverse_warp_file_path is None:
        inverse_warp_file = f""
    else:
        inverse_warp_file = f"-oinv {inverse_warp_file_path} "

    command_string = f"{system.GREEDY_PATH} " \
                     f"-d 3 " \
                     f"{initial_transform}" \
                     f"-i {reference_image_path} {moving_image_path} " \
                     f"-o {warp_file_path} " \
                     f"{inverse_warp_file}" \
                     f"-n {resolution_scheme} " \
                     f"-sv " \
                     f"-m {cost_function} "
    subprocess.run(command_string, shell=True, capture_output=c.SILENT_CMD)


def reslice_affine(reference_image: str, moving_image: str, resliced_image: str, affine_transform: str,
                   interpolation_type: str = "LABEL 0.2vox", background: float = 0.0):
    print(f"[OCELOT]      Reslicing {moving_image} -> {resliced_image}")
    print(f"[OCELOT]      Reference {reference_image} | Interpolation: {interpolation_type}")
    command_string = f"{system.GREEDY_PATH} " \
                     f"-d 3 " \
                     f"-rf {reference_image} " \
                     f"-ri {interpolation_type} " \
                     f"-rb {background} " \
                     f"-rm {moving_image} {resliced_image} " \
                     f"-r {affine_transform}"
    subprocess.run(command_string, shell=True, capture_output=c.SILENT_CMD)


def reslice_deformable(reference_image: str, moving_image: str, resliced_image: str, warp_transform: str,
                       affine_transform: str = None, interpolation_type: str = "LABEL 0.2vox", background: float = 0.0):
    print(f"[OCELOT]      Reslicing {moving_image} -> {resliced_image}")
    print(f"[OCELOT]      Reference {reference_image} | Interpolation: {interpolation_type}")

    if affine_transform is None:
        transforms = f"{warp_transform}"
    else:
        transforms = f"{warp_transform} {affine_transform}"

    command_string = f"{system.GREEDY_PATH} " \
                     f"-d 3 " \
                     f"-rf {reference_image} " \
                     f"-ri {interpolation_type} " \
                     f"-rb {background} " \
                     f"-rm {moving_image} {resliced_image} " \
                     f"-r {transforms}"
    subprocess.run(command_string, shell=True, capture_output=c.SILENT_CMD)


def reslice_deformable_inverse(reference_image: str, moving_image: str, resliced_image: str, inverse_warp_transform: str,
                               affine_transform: str = None, interpolation_type: str = "LABEL 0.2vox"):
    print(f"[OCELOT]      Reslicing {moving_image} -> {resliced_image}")
    print(f"[OCELOT]      Reference {reference_image} | Interpolation: {interpolation_type}")

    if affine_transform is None:
        inverse_transforms = f"{inverse_warp_transform}"
    else:
        inverse_transforms = f"{affine_transform},-1 {inverse_warp_transform}"

    command_string = f"{system.GREEDY_PATH} " \
                     f"-d 3 " \
                     f"-rf {reference_image} " \
                     f"-ri {interpolation_type} " \
                     f"-rm {moving_image} {resliced_image} " \
                     f"-r {inverse_transforms}"
    subprocess.run(command_string, shell=True, capture_output=c.SILENT_CMD)
