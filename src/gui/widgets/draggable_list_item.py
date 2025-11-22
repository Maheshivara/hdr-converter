from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtSvgWidgets import QSvgWidget

from os import path

from core.constants import Paths
from gui.widgets.effect_spin_box import EffectSpinBox, EffectInfo


class DraggableListItem(QWidget):
    def __init__(self, effect_box: EffectSpinBox):
        super().__init__()
        self.effect_box = effect_box
        layout = QHBoxLayout()
        layout.addWidget(self.effect_box)

        svg_path = path.join(Paths.ICONS_DIR, "drag_handle.svg")
        drag_handle = QSvgWidget(svg_path)
        drag_handle.setFixedSize(24, 24)
        layout.addWidget(drag_handle)

        self.setLayout(layout)

    def dragEnterEvent(self, event: QDragEnterEvent):
        event.accept()

    def dropEvent(self, event: QDropEvent):
        event.accept()

    def get_effect_info(self) -> EffectInfo:
        return self.effect_box.get_effect_info()
