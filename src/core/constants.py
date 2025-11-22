from os import path
import sys


class Paths:
    ROOT_DIR = (
        path.join(path.dirname(path.abspath(__file__)), "..", "..")
        if not getattr(sys, "frozen", False)
        else getattr(
            sys, "_MEIPASS", path.join(path.dirname(path.abspath(__file__)), "..", "..")
        )
    )
    ASSETS_DIR = path.join(ROOT_DIR, "assets")
    ICONS_DIR = path.join(ASSETS_DIR, "icons")
    LUTS_DIR = path.join(ASSETS_DIR, "LUTs")
