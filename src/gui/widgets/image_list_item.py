import os

from PySide6.QtWidgets import (
    QListWidgetItem,
    QWidget,
    QHBoxLayout,
    QLabel,
    QPushButton,
)

from gui.controllers.image_list import ImageListController


class ImageListItem(QListWidgetItem):
    def __init__(self, image_path: str, image_list_controller: ImageListController):
        super().__init__()
        self.image_path = image_path
        self.image_list_controller = image_list_controller

        self.widget = QWidget()
        self.layout = QHBoxLayout()
        self.widget.setLayout(self.layout)

        self.label = QLabel(os.path.basename(image_path))
        self.layout.addWidget(self.label)

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_image)
        self.layout.addWidget(self.delete_button)
        self.setSizeHint(self.widget.sizeHint())

    def delete_image(self):
        self.image_list_controller.remove_image(self.image_path)
