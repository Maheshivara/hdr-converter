import os
from typing import Tuple
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QGridLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QProgressBar,
    QListWidget,
)
from PySide6.QtCore import QThread


from gui.controllers.image_list import ImageListController
from gui.widgets.image_list_item import ImageListItem
from gui.widgets.rgbm_coefficient import RGBMCoefficientWidget
from gui.widgets.output_image_check import OutputImageCheckWidget
from gui.widgets.exposure_filter_box import ExposureFilterBox
from gui.workers.conversion import ConversionWorker


class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)

        layout = QGridLayout()
        self.grid_layout = layout
        self.setLayout(layout)

        self.selected_images_controller = ImageListController(
            lambda: self.update_image_list()
        )

        self.image_list_widget = QListWidget()
        layout.addWidget(self.image_list_widget, 0, 0, 4, 2)

        self.exposure_filter_box = ExposureFilterBox()
        layout.addWidget(self.exposure_filter_box, 0, 2, 1, 1)

        self.load_images_button = QPushButton("Load Images")
        self.load_images_button.clicked.connect(self.load_image)
        layout.addWidget(self.load_images_button, 4, 0)

        self.load_directory_button = QPushButton("Load Directory")
        self.load_directory_button.clicked.connect(self.load_directory)
        layout.addWidget(self.load_directory_button, 4, 1)

        self.rgbm_coefficient_widget = RGBMCoefficientWidget()
        layout.addWidget(self.rgbm_coefficient_widget, 5, 0, 1, 3)

        self.output_path_label = QLabel(
            f"Output Directory: {self.selected_images_controller.output_directory}"
        )
        layout.addWidget(self.output_path_label, 6, 0, 1, 2)

        self.output_path_button = QPushButton("Select Output Directory")
        self.output_path_button.clicked.connect(self.select_output_directory)
        layout.addWidget(self.output_path_button, 6, 2)

        self.output_image_check_widget = OutputImageCheckWidget()
        layout.addWidget(self.output_image_check_widget, 7, 0, 1, 3)

        self.to_rgbm_button = QPushButton("Convert to RGBM")
        self.to_rgbm_button.clicked.connect(self.convert_to_rgbm)
        layout.addWidget(self.to_rgbm_button, 8, 2, 1, 1)

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
                        f"Failed to select images.",
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
                    f"No supported images found in the selected directory.",
                )

    def update_image_list(self):
        self.image_list_widget.clear()
        for image_path in self.selected_images_controller.selected_images:
            item = ImageListItem(image_path, self.selected_images_controller)
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

        progress_bar = QProgressBar(self)
        progress_bar.setMaximum(len(self.selected_images_controller.selected_images))
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
            exposure=self._get_exposure(),
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

    def select_output_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            self.selected_images_controller.output_directory,
        )
        if directory:
            self.selected_images_controller.set_output_directory(directory)
            self.output_path_label.setText(f"Output Directory: {directory}")

    def on_conversion_finished(self, progress_bar: QProgressBar):
        self.to_rgbm_button.setEnabled(True)
        self.grid_layout.removeWidget(progress_bar)
        progress_bar.deleteLater()
        self.image_list_widget.clear()
        self.selected_images_controller.selected_images.clear()

    def _get_exposure(self) -> Tuple[bool, float]:
        return (
            self.exposure_filter_box.enabled_checkbox.isChecked(),
            self.exposure_filter_box.exposure_spinbox.value(),
        )
