import os

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QGridLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QProgressBar,
    QDoubleSpinBox,
    QListWidget,
)


from core.readers.image import ImageReader
from core.writers.image import ImageWriter
from core.encoders.rgbm import RGBMEncoder

from gui.controllers.image_list import ImageListController
from gui.widgets.image_list_item import ImageListItem


class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)

        layout = QGridLayout()
        self.grid_layout = layout
        self.setLayout(layout)

        self.image_reader = ImageReader()
        self.selected_images_controller = ImageListController(
            lambda: self.update_image_list()
        )

        self.image_list_widget = QListWidget()
        layout.addWidget(self.image_list_widget, 0, 0, 1, 2)

        self.load_images_button = QPushButton("Load Images")
        self.load_images_button.clicked.connect(self.load_image)
        layout.addWidget(self.load_images_button, 1, 0)

        self.load_directory_button = QPushButton("Load Directory")
        self.load_directory_button.clicked.connect(self.load_directory)
        layout.addWidget(self.load_directory_button, 1, 1)

        self.rgbm_coefficient_label = QLabel("RGBM Coefficient:")
        layout.addWidget(self.rgbm_coefficient_label, 4, 0)
        self.rgbm_coefficient_slider = QDoubleSpinBox()
        self.rgbm_coefficient_slider.setDecimals(4)
        self.rgbm_coefficient_slider.setSingleStep(0.1)
        self.rgbm_coefficient_slider.setMinimum(1e-6)
        self.rgbm_coefficient_slider.setMaximum(1e6)
        self.rgbm_coefficient_slider.setValue(8.0)
        layout.addWidget(self.rgbm_coefficient_slider, 4, 1)

        self.output_path_label = QLabel(
            f"Output Directory: {self.selected_images_controller.output_directory}"
        )
        layout.addWidget(self.output_path_label, 2, 0, 1, 2)

        self.output_path_button = QPushButton("Select Output Directory")
        self.output_path_button.clicked.connect(self.select_output_directory)
        layout.addWidget(self.output_path_button, 3, 0, 1, 2)

        self.to_rgbm_button = QPushButton("Convert to RGBM")
        self.to_rgbm_button.clicked.connect(self.convert_to_rgbm)
        layout.addWidget(self.to_rgbm_button, 5, 1, 1, 1)

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
        if self.rgbm_coefficient_slider.value() <= 0:
            QMessageBox.critical(
                self,
                "Error",
                "RGBM Coefficient must be greater than zero.",
            )
            return

        encoder = RGBMEncoder(self.rgbm_coefficient_slider.value())
        writer = ImageWriter()
        progress_bar = QProgressBar(self)
        progress_bar.setMaximum(len(self.selected_images_controller.selected_images))
        progress_bar.setValue(0)
        self.grid_layout.addWidget(progress_bar, 5, 0, 1, 1)

        for image_path in self.selected_images_controller.selected_images:
            image = self.image_reader.read_image(image_path)
            if image is None:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to read image: {image_path}",
                )
                continue

            rgbm_image = (
                encoder.from_exr(image)
                if image_path.lower().endswith(".exr")
                else encoder.from_hdr(image)
            )

            output_filename = (
                os.path.splitext(os.path.basename(image_path))[0] + "_rgbm.png"
            )
            output_filepath = os.path.join(
                self.selected_images_controller.output_directory, output_filename
            )
            writer.write_as_png(output_filepath, rgbm_image)
            progress_bar.setValue(progress_bar.value() + 1)
        self.image_list_widget.clear()

    def select_output_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            self.selected_images_controller.output_directory,
        )
        if directory:
            self.selected_images_controller.set_output_directory(directory)
            self.output_path_label.setText(f"Output Directory: {directory}")
