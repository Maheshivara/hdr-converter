from typing import List
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView

from gui.widgets.effect_spin_box import EffectSpinBox


class EffectsDragList(QListWidget):
    def __init__(self, effects: List[EffectSpinBox]):
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.effects = list(effects)

        for effect in self.effects:
            item = QListWidgetItem()
            item.setSizeHint(effect.sizeHint())
            self.addItem(item)
            self.setItemWidget(item, effect)

    def dropEvent(self, event):
        super().dropEvent(event)
        new_effects = []
        for i in range(self.count()):
            item = self.item(i)
            widget = self.itemWidget(item)
            if widget is not None:
                new_effects.append(widget)
        self.effects = new_effects
