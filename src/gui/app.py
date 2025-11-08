from PySide6.QtWidgets import QApplication

from gui.screens.home import HomeScreen


class HDRApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.setApplicationName("HDR Conversor")
        self.setOrganizationName("HJLW")
        self.setApplicationVersion("0.0.1")
        self.home_screen = HomeScreen()
