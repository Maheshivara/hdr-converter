from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QCheckBox, QSizePolicy
from PySide6.QtCore import Qt


class OutputImageCheckWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.image_format_label = QLabel("Output Image Format:")
        self.image_format_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.image_format_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(self.image_format_label)

        self.png_output_check_box = QCheckBox("PNG")
        self.png_output_check_box.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.png_output_check_box.setChecked(True)
        layout.addWidget(self.png_output_check_box)

        self.dds_output_check_box = QCheckBox("DDS")
        self.dds_output_check_box.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.dds_output_check_box.setChecked(False)
        layout.addWidget(self.dds_output_check_box)
