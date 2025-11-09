import numpy as np

from typing import Tuple


class EffectsTransformer:
    def _to_normalized(self, image: np.ndarray) -> Tuple[np.ndarray, bool]:
        img = image.astype(np.float32)
        was_255 = img.max() > 1.0
        if was_255:
            img = img / 255.0
        return img, was_255

    def _from_normalized(self, img: np.ndarray, was_255: bool) -> np.ndarray:
        img = np.clip(img, 0.0, 1.0)
        if was_255:
            return (img * 255.0).astype(np.uint8)
        return img.astype(np.float32)

    def apply_gamma_correction(self, image: np.ndarray, gamma: float) -> np.ndarray:
        img = np.clip(image.astype(np.float32), 0.0, 1.0)
        return np.power(img, 1.0 / gamma).astype(np.float32)

    def revert_gamma_correction(self, image: np.ndarray, gamma: float) -> np.ndarray:
        img = np.clip(image.astype(np.float32), 0.0, 1.0)
        return np.power(img, gamma).astype(np.uint8)

    def adjust_exposure(self, image: np.ndarray, exposure_value: float) -> np.ndarray:
        img, was_255 = self._to_normalized(image)
        factor = 2.0**exposure_value
        adjusted = np.clip(img * factor, 0.0, 1.0)
        return self._from_normalized(adjusted, was_255)

    def adjust_saturation(
        self, image: np.ndarray, saturation_factor: float
    ) -> np.ndarray:
        img, was_255 = self._to_normalized(image)
        lum = img[:, :, 0] * 0.2126 + img[:, :, 1] * 0.7152 + img[:, :, 2] * 0.0722
        result = (1.0 - saturation_factor) * lum[
            ..., np.newaxis
        ] + saturation_factor * img
        return self._from_normalized(result, was_255)

    def adjust_black_level(self, image: np.ndarray, black_level: float) -> np.ndarray:

        img, was_255 = self._to_normalized(image)
        bl_norm = float(black_level)
        if was_255 and bl_norm > 1.0:
            bl_norm = bl_norm / 255.0

        channels = img.shape[2]
        bl = np.full((1, 1, channels), bl_norm, dtype=np.float32)

        channel_max = np.max(img, axis=(0, 1), keepdims=True)
        denom = np.maximum(channel_max - bl, 1e-6)

        adjusted_linear = np.clip((img - bl) / denom, 0.0, 1.0)

        return self._from_normalized(adjusted_linear, was_255)
