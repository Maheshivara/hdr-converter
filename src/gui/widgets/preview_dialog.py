import os
from typing import Optional

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout


class PreviewDialog(QDialog):
    def __init__(
        self,
        image_path: str,
        rgbm_image: np.ndarray,
        parent: Optional[object] = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle(f"Preview - {os.path.basename(image_path)}")
        self.resize(800, 600)

        layout = QVBoxLayout(self)

        title = QLabel(os.path.basename(image_path), self)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self._image_label = QLabel(self)
        self._image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._image_label, stretch=1)

        button_row = QHBoxLayout()
        layout.addLayout(button_row)

        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.accept)
        button_row.addStretch(1)
        button_row.addWidget(close_button)
        button_row.addStretch(1)

        self._original_pixmap: Optional[QPixmap] = None
        self._set_image(rgbm_image)

    def _set_image(self, rgbm_image: np.ndarray) -> None:
        h, w, ch = rgbm_image.shape
        bytes_per_line = ch * w
        qimage = QImage(
            rgbm_image.data,
            w,
            h,
            bytes_per_line,
            QImage.Format_RGBA8888,
        )
        self._original_pixmap = QPixmap.fromImage(qimage)
        self._update_scaled_pixmap()

    def _update_scaled_pixmap(self) -> None:
        if self._original_pixmap is None:
            return
        scaled = self._original_pixmap.scaled(
            self._image_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self._image_label.setPixmap(scaled)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._update_scaled_pixmap()
