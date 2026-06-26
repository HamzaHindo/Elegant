import sys

from PySide6.QtWidgets import QApplication

from presentation.windows.main_window import MainWindow


def gui():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    gui()
