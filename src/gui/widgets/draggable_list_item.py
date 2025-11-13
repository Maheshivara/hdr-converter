from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtGui import QDragEnterEvent, QDropEvent

from gui.widgets.effect_spin_box import EffectSpinBox


class DraggableListItem(QWidget):
    def __init__(self, effect_box: EffectSpinBox):
        super().__init__()
        self.effect_box = effect_box
        layout = QVBoxLayout()
        layout.addWidget(self.effect_box)
        self.setLayout(layout)

    def dragEnterEvent(self, event: QDragEnterEvent):
        event.accept()

    def dropEvent(self, event: QDropEvent):
        event.accept()
