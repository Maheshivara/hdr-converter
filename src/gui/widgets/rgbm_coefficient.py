from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QDoubleSpinBox,
)


class RGBMCoefficientWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.rgbm_coefficient_label = QLabel("RGBM Coefficient:")
        layout.addWidget(self.rgbm_coefficient_label)

        self.rgbm_coefficient_input_box = QDoubleSpinBox()
        self.rgbm_coefficient_input_box.setDecimals(4)
        self.rgbm_coefficient_input_box.setSingleStep(0.1)
        self.rgbm_coefficient_input_box.setMinimum(1e-6)
        self.rgbm_coefficient_input_box.setMaximum(1e6)
        self.rgbm_coefficient_input_box.setValue(8.0)
        layout.addWidget(self.rgbm_coefficient_input_box)
