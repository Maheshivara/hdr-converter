from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QSizePolicy,
    QPushButton,
    QFileDialog,
    QMessageBox,
)
import os

from gui.controllers.image_list import ImageListController


class SelectFilesWidget(QWidget):
    def __init__(self, controller: ImageListController):
        super().__init__()
        self.selected_images_controller = controller
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QHBoxLayout()
        self.load_images_button = QPushButton("Load Images")
        self.load_images_button.clicked.connect(self._load_images)
        self.load_images_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        layout.addWidget(self.load_images_button)

        self.load_directory_button = QPushButton("Load Directory")
        self.load_directory_button.clicked.connect(self._load_directory)
        self.load_directory_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        layout.addWidget(self.load_directory_button)
        self.setLayout(layout)

    def _load_images(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
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

    def _load_directory(self):
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
