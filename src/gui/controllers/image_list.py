from typing import Callable, Set

from PySide6.QtCore import QStandardPaths


class ImageListController:
    def __init__(self, update_callback: Callable[[], None]):
        pictures_dir = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.PicturesLocation
        )
        if not pictures_dir:
            pictures_dir = ""
        self.output_directory = pictures_dir
        self.update_callback = update_callback
        self.selected_images: Set[str] = set()

    def add_image(self, image_path: str):
        self.selected_images.add(image_path)
        self.update_callback()

    def remove_image(self, image_path: str):
        self.selected_images.discard(image_path)
        self.update_callback()

    def set_output_directory(self, directory: str):
        self.output_directory = directory
