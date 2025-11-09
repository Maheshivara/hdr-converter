from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QCheckBox


class OutputImageCheckWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.image_format_label = QLabel("Output Image Format:")
        layout.addWidget(self.image_format_label)

        self.png_output_check_box = QCheckBox("PNG")
        self.png_output_check_box.setChecked(True)
        layout.addWidget(self.png_output_check_box)

        self.dds_output_check_box = QCheckBox("DDS")
        self.dds_output_check_box.setChecked(False)
        layout.addWidget(self.dds_output_check_box)
