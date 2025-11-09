import os

from PySide6.QtCore import QObject, Signal
from typing import Set, Tuple

from core.readers.image import ImageReader
from core.writers.image import ImageWriter
from core.encoders.rgbm import RGBMEncoder
from core.transformers.effects import EffectsTransformer

from gui.widgets.exposure_filter_box import ExposureFilterBox


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
        exposure: Tuple[bool, float],
        parent=None,
    ):
        super().__init__(parent)
        self.image_paths = image_paths
        self.output_directory = output_directory
        self.rgbm_coefficient = rgbm_coefficient
        self.to_png = to_png
        self.to_dds = to_dds
        self.exposure = exposure

        self.reader = ImageReader()
        self.writer = ImageWriter()
        self.transformer = EffectsTransformer()
        self.encoder = RGBMEncoder(self.rgbm_coefficient)

    def run(self):
        for idx, image_path in enumerate(self.image_paths, start=1):
            print(f"Processing image: {image_path}")
            try:
                image = self.reader.read_image(image_path)
                if image is None:
                    self.error.emit(f"Failed to read image: {image_path}")
                    continue

                rgbm_image = (
                    self.encoder.from_exr(image)
                    if image_path.lower().endswith(".exr")
                    else self.encoder.from_hdr(image)
                )

                exposure_enabled, exposure_value = self.exposure
                if exposure_enabled:
                    rgbm_image = self.transformer.adjust_exposure(
                        rgbm_image, exposure_value
                    )

                base = os.path.splitext(os.path.basename(image_path))[0]
                if self.to_dds:
                    output_filename = base + "_rgbm.dds"
                    output_filepath = os.path.join(
                        self.output_directory, output_filename
                    )
                    self.writer.write_as_dds(output_filepath, rgbm_image)

                if self.to_png:
                    output_filename = base + "_rgbm.png"
                    output_filepath = os.path.join(
                        self.output_directory, output_filename
                    )
                    self.writer.write_as_png(output_filepath, rgbm_image)

            except Exception as e:
                self.error.emit(str(e))

            self.progress.emit(idx)

        self.finished.emit()
