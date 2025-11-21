import os
from math import ceil

os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import cv2 as cv


class ImageReader:
    def read_image(self, filepath: str):
        return cv.imread(filepath, cv.IMREAD_UNCHANGED)

    def read_preview(self, filepath: str):
        image = self.read_image(filepath)
        if image is None:
            return None

        height, width = image.shape[:2]
        max_width = 1600
        max_height = 1024

        proportion = width / height
        new_width = width
        new_height = height

        if width > max_width:
            new_width = max_width
            new_height = ceil(new_width / proportion)

        if new_height > max_height:
            new_height = max_height
            new_width = ceil(new_height * proportion)

        preview_image = cv.resize(
            image, (new_width, new_height), interpolation=cv.INTER_AREA
        )
        return preview_image
