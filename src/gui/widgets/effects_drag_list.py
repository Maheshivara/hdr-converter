from typing import List
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView

from gui.widgets.effect_spin_box import EffectSpinBox
from gui.widgets.draggable_list_item import DraggableListItem


class EffectsDragList(QListWidget):
    def __init__(self, effects: List[EffectSpinBox]):
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.effects_items: List[DraggableListItem] = []
        for effect in effects:
            item = DraggableListItem(effect)
            list_item = QListWidgetItem(self)
            list_item.setSizeHint(item.sizeHint())
            self.addItem(list_item)
            self.setItemWidget(list_item, item)
            self.effects_items.append(item)
        self.setSizeAdjustPolicy(QListWidget.SizeAdjustPolicy.AdjustToContents)

    def dropEvent(self, event):
        super().dropEvent(event)
        self.selectionModel().clearSelection()
        self.setCurrentRow(-1)
        new_effects = []
        for i in range(self.count()):
            item = self.item(i)
            widget = self.itemWidget(item)
            if widget is not None:
                new_effects.append(widget)
        self.effects_items = new_effects
