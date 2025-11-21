import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from os import path


from gui.screens.home import HomeScreen


class HDRApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.setApplicationName("HDR Conversor")
        self.setOrganizationName("HJLW")
        self.setApplicationVersion("0.0.1")
        if getattr(sys, "frozen", False):
            base_dir = getattr(
                sys, "_MEIPASS", path.join(path.dirname(__file__), "..", "..")
            )
        else:
            base_dir = path.join(path.dirname(__file__), "..", "..")
        icon_path = path.join(base_dir, "assets", "icon.png")
        self.setWindowIcon(QIcon(icon_path))
        self.home_screen = HomeScreen()
