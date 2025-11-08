import os

import cv2 as cv


os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"


class ImageReader:
    def read_image(self, filepath: str):
        return cv.imread(filepath, cv.IMREAD_UNCHANGED)
