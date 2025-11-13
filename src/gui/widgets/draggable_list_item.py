import sys

from os import path
from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtSvgWidgets import QSvgWidget

from gui.widgets.effect_spin_box import EffectSpinBox


class DraggableListItem(QWidget):
    def __init__(self, effect_box: EffectSpinBox):
        super().__init__()
        self.effect_box = effect_box
        layout = QHBoxLayout()
        layout.addWidget(self.effect_box)

        if getattr(sys, "frozen", False):
            base_dir = getattr(
                sys, "_MEIPASS", path.join(path.dirname(__file__), "..", "..", "..")
            )
        else:
            base_dir = path.join(path.dirname(__file__), "..", "..", "..")
        svg_path = path.join(base_dir, "assets", "drag_handle.svg")
        drag_handle = QSvgWidget(svg_path)
        drag_handle.setFixedSize(24, 24)
        layout.addWidget(drag_handle)

        self.setLayout(layout)

    def dragEnterEvent(self, event: QDragEnterEvent):
        event.accept()

    def dropEvent(self, event: QDropEvent):
        event.accept()
