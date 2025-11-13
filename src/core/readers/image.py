import os

os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import cv2 as cv

class ImageReader:
    def read_image(self, filepath: str):
        return cv.imread(filepath, cv.IMREAD_UNCHANGED)
