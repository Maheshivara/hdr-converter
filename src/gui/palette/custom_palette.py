from PySide6.QtGui import QPalette
from os import path
import json

from core.constants import Paths


def get_custom_palette() -> QPalette:
    default_palette_path = path.join(Paths.PALETTES_DIR, "default.json")
    with open(default_palette_path, "r") as f:
        palette_data = json.load(f)["palette"]

    palette = QPalette()

    for role_name, color_hex in palette_data.items():
        role = getattr(QPalette, role_name, None)
        if role is not None:
            palette.setColor(role, color_hex)
    return palette
