from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QFileDialog,
)
from PySide6.QtCore import Qt

from gui.controllers.image_list import ImageListController


class OutputPathBox(QWidget):
    def __init__(self, image_controller: ImageListController):
        super().__init__()
        self.image_controller = image_controller
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.output_path_label = QLabel(
            f"Output Directory: {image_controller.output_directory}"
        )
        self.output_path_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.output_path_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(self.output_path_label)

        self.browse_button = QPushButton("Change...")
        self.browse_button.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.browse_button.clicked.connect(self.select_output_directory)
        self.browse_button.setFixedWidth(100)
        layout.addWidget(self.browse_button)

    def select_output_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            self.image_controller.output_directory,
        )
        if directory:
            self.image_controller.set_output_directory(directory)
            self.output_path_label.setText(f"Output Directory: {directory}")
