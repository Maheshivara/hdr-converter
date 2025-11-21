from typing import Set

import numpy as np
from PySide6.QtCore import Signal

from gui.workers.conversion import ConversionWorker, EffectInfo


class PreviewWorker(ConversionWorker):
    finished = Signal(np.ndarray)
    error = Signal(str)

    def __init__(
        self,
        image_path: str,
        rgbm_coefficient: float,
        effects: Set[EffectInfo],
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

    def run(self) -> None:
        try:
            rgbm_image = self._process_single_image(self._image_path)
            self.finished.emit(rgbm_image)
        except Exception as exc:
            self.error.emit(str(exc))
