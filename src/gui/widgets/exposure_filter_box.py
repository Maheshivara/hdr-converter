from PySide6.QtWidgets import QWidget, QCheckBox, QVBoxLayout, QLabel, QDoubleSpinBox
from PySide6.QtCore import Qt


class ExposureFilterBox(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.enabled_checkbox = QCheckBox("Enable Exposure Filter")
        self.enabled_checkbox.setChecked(False)
        layout.addWidget(self.enabled_checkbox)
        self.enabled_checkbox.stateChanged.connect(self.on_enabled_changed)

        self.label = QLabel("Exposure:")
        layout.addWidget(self.label)

        self.exposure_spinbox = QDoubleSpinBox()
        self.exposure_spinbox.setRange(0.0, 100)
        self.exposure_spinbox.setSingleStep(1.0)
        self.exposure_spinbox.setValue(0.0)
        layout.addWidget(self.exposure_spinbox)
        self.exposure_spinbox.setEnabled(False)

        self.setLayout(layout)

    def on_enabled_changed(self, state):
        self.exposure_spinbox.setEnabled(Qt.CheckState(state) == Qt.CheckState.Checked)
        self.exposure_spinbox.setValue(0.0)
