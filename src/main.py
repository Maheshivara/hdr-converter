import sys

from gui.app import HDRApp


def main():
    app = HDRApp(sys.argv)
    app.home_screen.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
