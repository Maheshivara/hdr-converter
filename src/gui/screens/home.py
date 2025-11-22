import os
from typing import List
from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QProgressBar,
    QListWidget,
    QSizePolicy,
)
from PySide6.QtCore import QThread, Qt


from gui.controllers.image_list import ImageListController
from gui.widgets.image_list_item import ImageListItem
from gui.widgets.preview_dialog import PreviewDialog
from gui.widgets.rgbm_coefficient import RGBMCoefficientWidget
from gui.widgets.output_image_check import OutputImageCheckWidget
from gui.widgets.effect_spin_box import EffectSpinBox
from gui.widgets.effects_drag_list import EffectsDragList
from gui.widgets.output_path_box import OutputPathBox
from gui.workers.conversion import ConversionWorker
from gui.workers.preview import PreviewWorker

from core.enums.effect_id import EffectID
from core.transformers.effects import EffectInfo


class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)

        layout = QGridLayout()
        self.grid_layout = layout
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 0)
        layout.setHorizontalSpacing(10)
        layout.setContentsMargins(8, 8, 8, 8)
        self.setLayout(layout)

        self.selected_images_controller = ImageListController(
            lambda: self.update_image_list()
        )

        self.image_list_widget = QListWidget()
        self.image_list_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        layout.addWidget(self.image_list_widget, 0, 0, 4, 3)

        self.exposure_filter_box = EffectSpinBox(
            EffectID.EXPOSURE,
            "Enable Exposure Filter",
            "Exposure:",
            -100,
            100,
            1.0,
            0.0,
        )

        self.black_level_filter_box = EffectSpinBox(
            EffectID.BLACK_LEVEL,
            "Enable Black Level Filter",
            "Black Level:",
            0.01,
            1.0,
            0.01,
            0.1,
        )

        self.saturation_filter_box = EffectSpinBox(
            EffectID.SATURATION,
            "Enable Saturation Filter",
            "Saturation:",
            0.1,
            5.0,
            0.1,
            1.0,
        )
        self.effects_drag_list = EffectsDragList(
            [
                self.exposure_filter_box,
                self.black_level_filter_box,
                self.saturation_filter_box,
            ]
        )
        self.effects_drag_list.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        layout.addWidget(self.effects_drag_list, 0, 3, 4, 1)

        self.load_images_button = QPushButton("Load Images")
        self.load_images_button.clicked.connect(self.load_image)
        self.load_images_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        layout.addWidget(self.load_images_button, 4, 0)

        self.load_directory_button = QPushButton("Load Directory")
        self.load_directory_button.clicked.connect(self.load_directory)
        self.load_directory_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        layout.addWidget(self.load_directory_button, 4, 1)

        self.rgbm_coefficient_widget = RGBMCoefficientWidget()
        self.rgbm_coefficient_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        layout.addWidget(self.rgbm_coefficient_widget, 5, 0, 1, 3)

        self.output_path_box = OutputPathBox(self.selected_images_controller)
        layout.addWidget(self.output_path_box, 6, 0, 1, 3)

        self.output_image_check_widget = OutputImageCheckWidget()
        self.output_image_check_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        layout.addWidget(self.output_image_check_widget, 7, 0, 1, 4)

        self.to_rgbm_button = QPushButton("Convert to RGBM")
        self.to_rgbm_button.clicked.connect(self.convert_to_rgbm)
        layout.addWidget(self.to_rgbm_button, 8, 3, 1, 1)

    def load_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("HDR Images (*.exr *.hdr)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                for image_path in selected_files:
                    if (
                        image_path
                        not in self.selected_images_controller.selected_images
                    ):
                        self.selected_images_controller.add_image(image_path)

                if not self.selected_images_controller.selected_images:
                    QMessageBox.critical(
                        self,
                        "Error",
                        "Failed to select images.",
                    )

    def load_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Image Directory",
            "",
        )
        if directory:
            supported_extensions = (".exr", ".hdr")
            for filename in os.listdir(directory):
                if filename.lower().endswith(supported_extensions):
                    image_path = os.path.join(directory, filename)
                    if (
                        image_path
                        not in self.selected_images_controller.selected_images
                    ):
                        self.selected_images_controller.add_image(image_path)

            if not self.selected_images_controller.selected_images:
                QMessageBox.critical(
                    self,
                    "Error",
                    "No supported images found in the selected directory.",
                )

    def update_image_list(self):
        self.image_list_widget.clear()
        for image_path in self.selected_images_controller.selected_images:
            item = ImageListItem(
                image_path,
                self.selected_images_controller,
                preview_callback=self.preview_image,
            )
            self.image_list_widget.addItem(item)
            self.image_list_widget.setItemWidget(item, item.widget)

    def convert_to_rgbm(self):
        rgbm_coefficient = (
            self.rgbm_coefficient_widget.rgbm_coefficient_input_box.value()
        )
        to_png = self.output_image_check_widget.png_output_check_box.isChecked()
        to_dds = self.output_image_check_widget.dds_output_check_box.isChecked()

        if not self.selected_images_controller.selected_images:
            QMessageBox.warning(self, "Warning", "No images selected for conversion.")
            return

        if not os.path.isdir(self.selected_images_controller.output_directory):
            QMessageBox.critical(
                self,
                "Error",
                "The specified output directory does not exist.",
            )
            return

        if not to_png and not to_dds:
            QMessageBox.critical(
                self,
                "Error",
                "At least one output format (PNG or DDS) must be selected.",
            )
            return

        if rgbm_coefficient <= 0:
            QMessageBox.critical(
                self,
                "Error",
                "RGBM Coefficient must be greater than zero.",
            )
            return

        if self.black_level_filter_box.enabled_checkbox.isChecked() and (
            self.black_level_filter_box.effect_spinbox.value() <= 0.0
            or self.black_level_filter_box.effect_spinbox.value() > 1.0
        ):
            QMessageBox.critical(
                self,
                "Error",
                "Black level must be in the range (0, 1].",
            )
            return

        image_count = len(self.selected_images_controller.selected_images)
        if (
            self.output_image_check_widget.png_output_check_box.isChecked()
            and self.output_image_check_widget.dds_output_check_box.isChecked()
        ):
            image_count *= 2
        progress_bar = QProgressBar(self)
        progress_bar.setMaximum(image_count)
        progress_bar.setValue(0)
        self.grid_layout.addWidget(progress_bar, 9, 0, 1, 3)

        self.to_rgbm_button.setEnabled(False)

        thread = QThread(self)
        worker = ConversionWorker(
            image_paths=self.selected_images_controller.selected_images,
            output_directory=self.selected_images_controller.output_directory,
            rgbm_coefficient=rgbm_coefficient,
            to_png=to_png,
            to_dds=to_dds,
            effects=self._get_effects(),
        )
        worker.progress.connect(progress_bar.setValue)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(
            lambda: QMessageBox.information(self, "Info", "Conversion completed.")
        )
        worker.finished.connect(lambda: self.on_conversion_finished(progress_bar))
        worker.error.connect(lambda msg: QMessageBox.critical(self, "Error", msg))

        self._conversor_worker = worker
        self._conversion_thread = thread

        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        thread.start()

    def on_conversion_finished(self, progress_bar: QProgressBar):
        self.to_rgbm_button.setEnabled(True)
        self.grid_layout.removeWidget(progress_bar)
        progress_bar.deleteLater()
        self.image_list_widget.clear()
        self.selected_images_controller.selected_images.clear()

    def _get_effects(self) -> List[EffectInfo]:
        effects = []
        for e in self.effects_drag_list.effects_items:
            effects.append(e.get_effect_info())
        return effects

    def preview_image(self, image_path: str):
        """Processa a imagem selecionada e mostra um preview RGBM sem salvar."""
        rgbm_coefficient = (
            self.rgbm_coefficient_widget.rgbm_coefficient_input_box.value()
        )

        if rgbm_coefficient <= 0:
            QMessageBox.critical(
                self,
                "Error",
                "RGBM Coefficient must be greater than zero.",
            )
            return

        if self.black_level_filter_box.enabled_checkbox.isChecked() and (
            self.black_level_filter_box.effect_spinbox.value() <= 0.0
            or self.black_level_filter_box.effect_spinbox.value() > 1.0
        ):
            QMessageBox.critical(
                self,
                "Error",
                "Black level must be in the range (0, 1].",
            )
            return

        thread = QThread(self)
        worker = PreviewWorker(
            image_path=image_path,
            rgbm_coefficient=rgbm_coefficient,
            effects=self._get_effects(),
        )

        # guardar o caminho atual para uso no slot de preview
        self._last_preview_image_path = image_path

        worker.finished.connect(
            self._on_preview_finished,
            Qt.ConnectionType.QueuedConnection,
        )
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        worker.error.connect(lambda msg: QMessageBox.critical(self, "Error", msg))

        # manter referências para evitar coleta de lixo enquanto a thread roda
        self._preview_worker = worker
        self._preview_thread = thread

        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        thread.start()

    def _on_preview_finished(self, rgbm_image):
        """Slot chamado quando o PreviewWorker termina o processamento."""
        image_path = getattr(self, "_last_preview_image_path", "")
        dialog = PreviewDialog(image_path, rgbm_image, self)
        dialog.exec()
