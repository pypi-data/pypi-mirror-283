# ------------------------------------------------------ Imports ----------------------------------------------------- #
import zipfile
import requests
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, FileSizeColumn, TransferSpeedColumn
import os

from ocelotz import system
from ocelotz import constants
from ocelotz import file_management


# ----------------------------------------------------- Constants ---------------------------------------------------- #
OCELOT_BINARIES = {
    "ocelot-windows-x86_64": {
        "url": "https://enhance-pet.s3.eu-central-1.amazonaws.com/awesome/beast-binaries-windows-x86_64.zip",
        "filename": "beast-binaries-windows-x86_64.zip",
        "directory": "beast-binaries-windows-x86_64",
    },
    "ocelot-linux-x86_64": {
        "url": "https://enhance-pet.s3.eu-central-1.amazonaws.com/awesome/beast-binaries-linux-x86_64.zip",
        "filename": "beast-binaries-linux-x86_64.zip",
        "directory": "beast-binaries-linux-x86_64",
    },
    "ocelot-mac-x86_64": {
        "url": "https://enhance-pet.s3.eu-central-1.amazonaws.com/awesome/beast-binaries-mac-x86_64.zip",
        "filename": "beast-binaries-mac-x86_64.zip",
        "directory": "beast-binaries-mac-x86_64",
    },
    "ocelot-mac-arm64": {
        "url": "https://enhance-pet.s3.eu-central-1.amazonaws.com/awesome/beast-binaries-mac-arm64.zip",
        "filename": "beast-binaries-mac-arm64.zip",
        "directory": "beast-binaries-mac-arm64",
    },
}


def binaries():
    system_os = system.get_operating_system()
    system_arch = system.get_architecture()
    if system_os == 'windows':
        file_management.create_directory(system.BINARY_PATH)

    binaries_to_download = f'ocelot-{system_os}-{system_arch}'
    binaries_info = OCELOT_BINARIES[binaries_to_download]
    url = binaries_info["url"]
    filename = os.path.join(system.BINARY_PATH, binaries_info["filename"])
    directory = os.path.join(system.BINARY_PATH, binaries_info["directory"])

    if not os.path.exists(directory):
        print(f" Downloading {directory}")

        # show progress using rich
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get("Content-Length", 0))
        chunk_size = 1024 * 10

        console = Console()
        progress = Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.0f}%", "•",
            FileSizeColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            console=console,
            expand=True
        )

        with progress:
            task = progress.add_task(f"[white] Downloading system specific binaries: {binaries_to_download}", total=total_size)
            for chunk in response.iter_content(chunk_size=chunk_size):
                open(filename, "ab").write(chunk)
                progress.update(task, advance=chunk_size)

        # Unzip the item
        progress = Progress(  # Create new instance for extraction task
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.0f}%", "•",
            FileSizeColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            console=console,
            expand=True
        )

        with progress:
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                total_size = sum((file.file_size for file in zip_ref.infolist()))
                task = progress.add_task(f"[white] Extracting system specific binaries: {binaries_to_download}",
                                         total=total_size)
                # Get the parent directory of 'directory'
                parent_directory = os.path.dirname(directory)
                for file in zip_ref.infolist():
                    zip_ref.extract(file, parent_directory)
                    extracted_size = file.file_size
                    progress.update(task, advance=extracted_size)

        print(f" {os.path.basename(directory)} extracted.")

        # Delete the zip file
        os.remove(filename)
        print(f"{constants.ANSI_GREEN} Binaries - download complete. {constants.ANSI_RESET}\n")
    else:
        print(f"{constants.ANSI_GREEN} A local instance of {binaries_to_download} binaries has been detected. "
              f"{constants.ANSI_RESET}\n")

    system.set_permissions(system.GREEDY_PATH, system_os)
    system.set_permissions(system.DCM2NIIX_PATH, system_os)
