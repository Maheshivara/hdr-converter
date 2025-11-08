import numpy as np


class EffectsTransformer:
    def apply_gamma_correction(self, image: np.ndarray, gamma: float) -> np.ndarray:
        img = image.astype(np.float32)
        gamma_corrected = (img ** (1.0 / gamma)).astype(np.float32)
        return gamma_corrected

    def revert_gamma_correction(self, image: np.ndarray, gamma: float) -> np.ndarray:
        img = image.astype(np.float32)
        gamma_corrected = (img**gamma).astype(np.float32)
        return gamma_corrected

    def adjust_exposure(self, image: np.ndarray, exposure_value: float) -> np.ndarray:
        factor = 2.0**exposure_value
        adjusted_image = np.clip(image * factor, 0.0, None)
        return adjusted_image

    def adjust_saturation(
        self, image: np.ndarray, saturation_factor: float
    ) -> np.ndarray:
        img = image.astype(np.float32)
        lum = img[:, :, 0] * 0.2126 + img[:, :, 1] * 0.7152 + img[:, :, 2] * 0.0722
        result = (1.0 - saturation_factor) * lum[
            ..., np.newaxis
        ] + saturation_factor * img
        return result

    def adjust_black_level(self, image: np.ndarray, black_level: float) -> np.ndarray:
        img = self.apply_gamma_correction(image, gamma=2.2)

        channel_max = np.max(img, axis=(0, 1), keepdims=True)

        bl = np.full((1, 1, img.shape[2]), black_level, dtype=np.float32)

        denom = np.maximum(channel_max - bl, 1e-6)
        adjusted_image = np.clip((img - bl) / denom, 0.0, None)
        output = self.revert_gamma_correction(adjusted_image, gamma=2.2)

        return output
