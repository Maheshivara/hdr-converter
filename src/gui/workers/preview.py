from typing import List

import numpy as np
from PySide6.QtCore import Signal

from core.readers.image import ImageReader
from core.transformers.effects import EffectInfo
from gui.workers.conversion import ConversionWorker


class PreviewWorker(ConversionWorker):
    finished = Signal(np.ndarray)
    error = Signal(str)

    def __init__(
        self,
        image_path: str,
        rgbm_coefficient: float,
        effects: List[EffectInfo],
        parent=None,
    ) -> None:
        super().__init__(
            image_paths={image_path},
            output_directory="",
            rgbm_coefficient=rgbm_coefficient,
            to_png=False,
            to_dds=False,
            effects=effects,
            parent=parent,
        )
        self._image_path = image_path
        self.reader = ImageReader()

    def _process_single_image(self, image_path: str):
        """Versão de preview: lê imagem redimensionada antes de aplicar efeitos/encoder."""
        image = self.reader.read_preview(image_path)
        if image is None:
            raise RuntimeError(f"Failed to read image: {image_path}")

        image = self.transformer.apply_effects(image, self.effects)
        return image

    def run(self) -> None:
        try:
            rgbm_image = self._process_single_image(self._image_path)
            self.finished.emit(rgbm_image)
        except Exception as exc:
            self.error.emit(str(exc))
