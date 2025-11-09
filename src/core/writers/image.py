import numpy as np
import cv2 as cv
from wand.image import Image as WandImage


class ImageWriter:
    def write_as_png(self, filepath: str, image: np.ndarray):
        filepath = filepath if filepath.lower().endswith(".png") else filepath + ".png"
        if image is not None:
            cv.imwrite(filepath, image)

    def write_as_dds(self, filepath: str, image: np.ndarray):
        filepath = filepath if filepath.lower().endswith(".dds") else filepath + ".dds"
        if image is None:
            return
        img = cv.cvtColor(image, cv.COLOR_RGB2BGRA)
        with WandImage.from_array(img) as wand_image:
            wand_image.compression = "dxt5"
            wand_image.save(filename=filepath)
