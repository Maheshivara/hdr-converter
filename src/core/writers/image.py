import numpy as np
import os
os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import cv2 as cv
from PIL import Image


class ImageWriter:
    def write_as_png(self, filepath: str, image: np.ndarray):
        filepath = filepath if filepath.lower().endswith(".png") else filepath + ".png"
        if image is not None:
            cv.imwrite(filepath, image)

    def write_as_dds(self, filepath: str, image: np.ndarray):
        filepath = filepath if filepath.lower().endswith(".dds") else filepath + ".dds"
        img = cv.cvtColor(image, cv.COLOR_RGB2BGRA)
        if image is not None:
            pil_image = Image.fromarray(img)
            pil_image.save(filepath, pixel_format="DXT5")
