from os import path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from core.constants import Paths

from gui.screens.home import HomeScreen


class HDRApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.setApplicationName("HDR Converter")
        self.setOrganizationName("HJLW")
        self.setApplicationVersion("0.0.1")

        icon_path = path.join(Paths.ICONS_DIR, "icon.png")
        self.setWindowIcon(QIcon(icon_path))
        self.home_screen = HomeScreen()
