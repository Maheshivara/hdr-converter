import os

from PySide6.QtWidgets import (
    QListWidgetItem,
    QWidget,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
)

from gui.controllers.image_list import ImageListController


class ImageListItem(QListWidgetItem):
    def __init__(
        self,
        image_path: str,
        image_list_controller: ImageListController,
        preview_callback=None,
    ):
        super().__init__()
        self.image_path = image_path
        self.image_list_controller = image_list_controller
        self.preview_callback = preview_callback

        self.widget = QWidget()
        self.layout = QHBoxLayout()
        self.widget.setLayout(self.layout)

        self.label = QLabel(os.path.basename(image_path))
        self.layout.addWidget(self.label)

        self.preview_button = QPushButton("Preview")
        self.preview_button.clicked.connect(self.preview_image)
        self.layout.addWidget(self.preview_button)

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_image)
        self.layout.addWidget(self.delete_button)
        self.setSizeHint(self.widget.sizeHint())

    def preview_image(self):
        if self.preview_callback is not None:
            try:
                self.preview_callback(self.image_path)
            except Exception as e:
                QMessageBox.critical(
                    self.widget, "Error", f"Error previewing image: {e}"
                )

    def delete_image(self):
        self.image_list_controller.remove_image(self.image_path)
