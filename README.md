# HDR Converter

## Description
This is a basic application that uses the libraries [OpenCV](https://pypi.org/project/opencv-python/) and [OpenEXR](https://pypi.org/project/OpenEXR/) to convert HDR images (`.hdr` and `.exr`) to RGBM, following the steps described [here](https://graphicrants.blogspot.com/2009/04/rgbm-color-encoding.html) by Brian Karis.

The application was developed as part of the *Digital Processing of Images and Signals* course during the 2025.2 term at the *Instituto Federal de Alagoas (IFAL) - Campus Arapiraca*, taught by Professor **Edvonaldo Horácio dos Santos, M.Sc.**

The group of contributors:
- [Humberto Augusto](https://github.com/Humberto0003)
- [José Bezerra](https://github.com/JBPinheiro86)
- [Luis Gabriel](https://github.com/Maheshivara)
- [Wallace Souza](https://github.com/RochaSWallace)

## How to Run
> [!IMPORTANT]  
> This project uses [uv](https://docs.astral.sh/uv/) as its package manager. All steps described below assume that you have it installed and configured.

> [!IMPORTANT]  
> You will also need Python version **3.14** (or later). You can install it with the command:
> ```sh
> uv python install 3.14
> ```

1. Clone this repository to your desired location.  
2. Inside the cloned repository directory, synchronize the project dependencies with:
    ```sh
    uv sync
    ```
3. Start the UI with:
    ```sh
    uv run src/main.py
    ```
## How to Build

> [!IMPORTANT]  
> The build system for this project uses the [PyInstaller](https://pyinstaller.org/en/stable/index.html) tool. For a successful build, you need to sync the project first using the `uv sync` command.

1. Run the PyInstaller command with the `.spec` file available in this repository:
    ```sh
    uv run pyinstaller main.spec
    ```

2. The bundled file will be located in the `dist` directory (in the root directory):
    1. For Linux, the binary will be named `main`.
        1. Remember to give execute permissions before running it with:
            ```sh
            chmod +x ./main
            ```
    2. For Windows, the file will be named `main.exe`.
    3. We do not have a Mac to build, but the name should be `main`, as on Linux