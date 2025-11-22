import os

from PySide6.QtCore import QObject, Signal
from typing import List, Set

from core.readers.image import ImageReader
from core.writers.image import ImageWriter
from core.encoders.rgbm import RGBMEncoder
from core.transformers.effects import EffectsTransformer, EffectInfo


class ConversionWorker(QObject):
    progress = Signal(int)
    finished = Signal()
    error = Signal(str)

    def __init__(
        self,
        image_paths: Set[str],
        output_directory: str,
        rgbm_coefficient: float,
        to_png: bool,
        to_dds: bool,
        effects: List[EffectInfo],
        parent=None,
    ):
        super().__init__(parent)
        self.image_paths = image_paths
        self.output_directory = output_directory
        self.rgbm_coefficient = rgbm_coefficient
        self.to_png = to_png
        self.to_dds = to_dds
        self.effects = effects

        self.reader = ImageReader()
        self.writer = ImageWriter()
        self.transformer = EffectsTransformer()
        self.encoder = RGBMEncoder(self.rgbm_coefficient)

    def _process_single_image(self, image_path: str):
        """Lê, aplica efeitos e converte uma única imagem para RGBM."""
        image = self.reader.read_image(image_path)
        if image is None:
            raise RuntimeError(f"Failed to read image: {image_path}")

        image = self.transformer.apply_effects(image, self.effects)

        rgbm_image = (
            self.encoder.from_exr(image)
            if image_path.lower().endswith(".exr")
            else self.encoder.from_hdr(image)
        )
        return rgbm_image

    def run(self):
        img_count = 0
        for image_path in self.image_paths:
            try:
                rgbm_image = self._process_single_image(image_path)

                base = os.path.splitext(os.path.basename(image_path))[0]
                if self.to_dds:
                    output_filename = base + "_rgbm.dds"
                    output_filepath = os.path.join(
                        self.output_directory, output_filename
                    )
                    self.writer.write_as_dds(output_filepath, rgbm_image)
                    img_count += 1
                    self.progress.emit(img_count)

                if self.to_png:
                    output_filename = base + "_rgbm.png"
                    output_filepath = os.path.join(
                        self.output_directory, output_filename
                    )
                    self.writer.write_as_png(output_filepath, rgbm_image)
                    img_count += 1
                    self.progress.emit(img_count)

            except Exception as e:
                self.error.emit(str(e))

        self.finished.emit()
