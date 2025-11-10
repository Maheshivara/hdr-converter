import numpy as np

from typing import Tuple


class EffectsTransformer:
    def apply_gamma_correction(self, image: np.ndarray, gamma: float) -> np.ndarray:
        if gamma <= 0.0:
            raise ValueError("Gamma must be greater than 0.")
        img = np.clip(image.astype(np.float32), 0.0, 1.0)
        return np.power(img, 1.0 / gamma).astype(np.float32)

    def revert_gamma_correction(self, image: np.ndarray, gamma: float) -> np.ndarray:
        if gamma <= 0.0:
            raise ValueError("Gamma must be greater than 0.")
        img = np.clip(image.astype(np.float32), 0.0, 1.0)
        reverted = np.power(img, gamma).astype(np.float32)
        return reverted

    def adjust_exposure(self, image: np.ndarray, exposure_value: float) -> np.ndarray:
        factor = 2.0**exposure_value
        adjusted = np.clip(image * factor, 0.0, 1.0)
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
        if black_level <= 0.0 or black_level > 1.0:
            raise ValueError("Black level must be in the range (0, 1].")

        channels = image.shape[2]
        bl = np.full((1, 1, channels), black_level, dtype=np.float32)

        channel_max = np.max(image, axis=(0, 1), keepdims=True)
        denom = np.maximum(channel_max - bl, 1e-6)

        adjusted = np.clip((image - bl) / denom, 0.0, 1.0)

        return adjusted
