from PySide6.QtGui import QFont, QFontDatabase
from os import path

from core.constants import Paths


def load_font() -> QFont:
    default_font_path = path.join(Paths.FONTS_DIR, "OpenSans-Regular.ttf")
    font_id = QFontDatabase.addApplicationFont(default_font_path)
    font_families = QFontDatabase.applicationFontFamilies(font_id)
    if font_families:
        font_family = font_families[0]
        return QFont(font_family)
    else:
        raise RuntimeError(f"Failed to load font from {default_font_path}")
