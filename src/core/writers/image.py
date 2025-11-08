import numpy as np
import cv2 as cv


class ImageWriter:
    def write_as_png(self, filepath: str, image: np.ndarray):
        filepath = filepath if filepath.lower().endswith(".png") else filepath + ".png"
        if image is not None:
            cv.imwrite(filepath, image)
