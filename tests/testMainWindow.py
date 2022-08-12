import sys
from PyQt5 import QtWidgets
from challenger.mainWindow import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # apply_stylesheet(app, theme= "dark_amber.xml")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
