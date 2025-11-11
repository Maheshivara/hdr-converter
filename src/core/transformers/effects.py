import numpy as np


class EffectsTransformer:
    def apply_gamma_correction(self, image: np.ndarray, gamma: float) -> np.ndarray:
        if gamma <= 0.0:
            raise ValueError("Gamma must be greater than 0.")
        return np.power(image.astype(np.float32), 1.0 / gamma)

    def revert_gamma_correction(self, image: np.ndarray, gamma: float) -> np.ndarray:
        if gamma <= 0.0:
            raise ValueError("Gamma must be greater than 0.")
        reverted = np.power(image.astype(np.float32), gamma)
        return reverted

    def adjust_exposure(self, image: np.ndarray, exposure_value: float) -> np.ndarray:
        factor = 2.0**exposure_value
        adjusted = image.astype(np.float32) * factor
        return adjusted

    def adjust_saturation(
        self, image: np.ndarray, saturation_factor: float
    ) -> np.ndarray:
        lum = (
            image[:, :, 0] * 0.2126 + image[:, :, 1] * 0.7152 + image[:, :, 2] * 0.0722
        )
        result = (1.0 - saturation_factor) * lum[
            ..., np.newaxis
        ] + saturation_factor * image
        return result

    def adjust_black_level(self, image: np.ndarray, black_level: float) -> np.ndarray:
        if black_level < 0.0 or black_level > 1.0:
            raise ValueError("Black level must be in the range [0, 1].")
        img = image.astype(np.float32)

        max_red = np.max(img[:, :, 0])
        max_green = np.max(img[:, :, 1])
        max_blue = np.max(img[:, :, 2])

        adjusted = np.zeros_like(img)
        adjusted[:, :, 0] = np.maximum(
            (img[:, :, 0] - black_level) / (max_red - black_level), 0
        )
        adjusted[:, :, 1] = np.maximum(
            (img[:, :, 1] - black_level) / (max_green - black_level), 0
        )
        adjusted[:, :, 2] = np.maximum(
            (img[:, :, 2] - black_level) / (max_blue - black_level), 0
        )
        if img.shape[2] == 4:
            adjusted[:, :, 3] = img[:, :, 3]

        return adjusted
