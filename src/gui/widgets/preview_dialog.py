import os
from typing import Optional

import cv2 as cv
import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
)

from core.transformers.lut import LutTransformer


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

        # Barra de botões abaixo da imagem
        controls_row = QHBoxLayout()
        layout.addLayout(controls_row)

        self._load_lut_button = QPushButton("Carregar LUT…", self)
        self._load_lut_button.clicked.connect(self._on_load_lut_clicked)
        controls_row.addStretch(1)
        controls_row.addWidget(self._load_lut_button)
        controls_row.addStretch(1)

        button_row = QHBoxLayout()
        layout.addLayout(button_row)

        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.accept)
        button_row.addStretch(1)
        button_row.addWidget(close_button)
        button_row.addStretch(1)

        self._original_pixmap: Optional[QPixmap] = None
        self._base_image: np.ndarray = rgbm_image
        self._current_lut: Optional[LutTransformer] = None

        # Carrega LUT padrão (assets/AgX.png), se disponível
        self._apply_default_lut()

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

    def _apply_default_lut(self) -> None:
        """Carrega e aplica a LUT padrão (assets/AgX.png) se existir.

        Caso a LUT não seja encontrada, mostra a imagem base sem LUT.
        """

        lut_path = os.path.join("assets", "AgX.png")
        if not os.path.exists(lut_path):
            # Sem LUT padrão, mostra apenas a imagem base
            self._set_image(self._base_image)
            return

        lut_img = cv.imread(lut_path, cv.IMREAD_UNCHANGED)
        if lut_img is None:
            self._set_image(self._base_image)
            return

        self._current_lut = LutTransformer(lut_img)
        self._apply_current_lut()

    def _apply_current_lut(self) -> None:
        """Aplica a LUT atual (se houver) sobre a imagem base e atualiza a view."""

        if self._current_lut is None:
            self._set_image(self._base_image)
            return

        # Aplica LUT sobre a imagem base
        lut_image = self._current_lut.apply(self._base_image)

        # Garante formato uint8 RGBA para o QImage, se necessário
        if lut_image.dtype != np.uint8:
            lut_image = np.clip(lut_image * 255.0, 0, 255).astype(np.uint8)

        # Se vier RGB, converte para RGBA adicionando alpha=255
        if lut_image.shape[2] == 3:
            alpha = np.full(lut_image.shape[:2] + (1,), 255, dtype=np.uint8)
            lut_image = np.concatenate([lut_image, alpha], axis=2)

        self._set_image(lut_image)

    def _on_load_lut_clicked(self) -> None:
        """Permite ao usuário escolher uma nova imagem de LUT e reaplicar."""

        start_dir = os.path.join(os.getcwd(), "assets")
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar LUT",
            start_dir,
            "Imagens (*.png *.jpg *.jpeg *.tiff *.tif)",
        )
        if not filename:
            return

        lut_img = cv.imread(filename, cv.IMREAD_UNCHANGED)
        if lut_img is None:
            return

        self._current_lut = LutTransformer(lut_img)
        self._apply_current_lut()
