from PySide6.QtWidgets import QWidget, QCheckBox, QVBoxLayout, QLabel, QDoubleSpinBox
from PySide6.QtCore import Qt

from core.enums.effect_id import EffectID


class EffectSpinBox(QWidget):
    def __init__(
        self,
        effect_id: EffectID,
        checkbox_label: str,
        spinbox_label: str,
        min_value: float,
        max_value: float,
        step: float,
        default_value: float,
    ):
        super().__init__()

        self.default_value = default_value
        self.effect_id = effect_id

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.enabled_checkbox = QCheckBox(checkbox_label)
        self.enabled_checkbox.setChecked(False)
        layout.addWidget(self.enabled_checkbox)
        self.enabled_checkbox.stateChanged.connect(self.on_enabled_changed)

        self.label = QLabel(spinbox_label)
        layout.addWidget(self.label)

        self.effect_spinbox = QDoubleSpinBox()
        self.effect_spinbox.setRange(min_value, max_value)
        self.effect_spinbox.setSingleStep(step)
        self.effect_spinbox.setValue(default_value)
        layout.addWidget(self.effect_spinbox)
        self.effect_spinbox.setEnabled(False)

        self.setLayout(layout)

    def on_enabled_changed(self, state):
        self.effect_spinbox.setEnabled(Qt.CheckState(state) == Qt.CheckState.Checked)
        self.effect_spinbox.setValue(self.default_value)
