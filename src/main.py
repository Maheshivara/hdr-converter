import sys

from gui.app import HDRApp
from gui.palette.custom_palette import get_custom_palette
from gui.fonts.load_font import load_font


def main():
    app = HDRApp(sys.argv)
    font = load_font()
    app.setFont(font)
    app.setPalette(get_custom_palette())
    app.home_screen.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
