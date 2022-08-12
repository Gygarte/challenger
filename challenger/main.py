import sys
import os
from PyQt5 import QtWidgets
from challenger.gui import main_window
from PyQt5.QtCore import QThreadPool


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)

    # apply_stylesheet(app, theme= "dark_amber.xml")
    window = main_window.MainWindow(QThreadPool)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
