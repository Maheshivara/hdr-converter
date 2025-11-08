import numpy as np
from core.transformers.effects import EffectsTransformer


class RGBMEncoder:
    def __init__(self, coefficient: float) -> None:
        self.coefficient = coefficient
        self.effects_transformer = EffectsTransformer()

    def from_hdr(self, hdr_image: np.ndarray) -> np.ndarray:
        corrected_image = self.effects_transformer.apply_gamma_correction(
            hdr_image, gamma=2.2
        )

        color = corrected_image[..., :3] / self.coefficient

        alpha = np.maximum(
            np.maximum(color[..., 0], color[..., 1]), np.maximum(color[..., 2], 1e-6)
        )
        alpha = np.clip(alpha, 0.0, 1.0)

        alpha = np.ceil(alpha * 255.0) / 255.0

        alpha_exp = alpha[..., np.newaxis]
        rgb = color / alpha_exp

        encoded_image = np.concatenate([rgb, alpha_exp], axis=-1)

        output_image = np.clip(encoded_image, 0.0, 1.0) * 255

        return output_image.astype(np.uint8)

    def from_exr(self, input_img: np.ndarray) -> np.ndarray:
        exr_image = np.clip(input_img, 0.0, None)
        return self.from_hdr(exr_image)
