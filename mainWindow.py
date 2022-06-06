import pandas as pd
import os
from pathlib import Path
from PyQt5 import QtWidgets
from ui.mainWindow import Ui_MainWindow
from setting import DOC, DATABASE, OUTPUT


def readInputFileSheets(path_to_directory: str) -> list:
    df = pd.ExcelFile(os.path.join(Path(path_to_directory).resolve(), DOC))

    return df.sheet_names


# It creates a class called MainWindow that inherits from QMainWindow.
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None) -> None:
        QtWidgets.QMainWindow.__init__(self)
        self.window = Ui_MainWindow()
        self.window.setupUi(self)

        self.window.exit_botton.clicked.connect(lambda: self.close())
        self.window.add_botton.clicked.connect(lambda: self.addSignToDict())
        self.window.delete_botton.clicked.connect(lambda: self.deleteSignFromDict())
        self.window.run_botton.clicked.connect(lambda: self.callRunFunction())
        self.window.save_botton.clicked.connect(lambda: self.callPauseResumeFunction())
        self.window.select_input_path_button.clicked.connect(lambda: self.callSelectInputFolderDialog())

        # display default values from setting into corresponding fields
        self.window.doc_lineEdit.setText(DOC)
        self.window.database_lineEdit.setText(DATABASE)
        self.window.output_name_lineEdit.setText(OUTPUT)

    def addSignToDict(self) -> None:
        """
        It adds a row to a table widget.
        """
        row_count = self.window.sign_table.rowCount()
        self.window.sign_table.setRowCount(row_count + 1)
        self.window.sign_table.setColumnCount(2)
        self.window.sign_table.setHorizontalHeaderLabels(["Variable", "Sign"])

    def deleteSignFromDict(self) -> None:
        """
        It deletes the selected row from the table
        """
        row_number = self.window.sign_table.currentRow()
        self.window.sign_table.removeRow(row_number)

    def callRunFunction(self) -> None:
        input_folder = self.readInputLineEdit()
        portfolio = self.readPortfolioLineEdit()

    def callPauseResumeFunction(self) -> None:
        pass

    def callSelectInputFolderDialog(self) -> None:
        """
        It opens a file dialog and sets the text of a lineEdit widget to the path of the selected
        directory
        """
        input_directory_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Input Directory')

        input_sheets = readInputFileSheets(input_directory_path)

        self.window.portfolio_comboBox.addItems(input_sheets)

        self.window.input_lineEdit.setText(input_directory_path)

    def readInputLineEdit(self) -> str:
        """
        If the input_lineEdit is empty, set the error color, otherwise reset the error color and return
        the input_lineEdit text
        :return: The input_element is being returned.
        """
        input_element = self.window.input_lineEdit.text()

        if input_element in "":
            self.setErrorColor(self.window.input_lineEdit)
        else:
            self.resetErrorColor(self.window.input_lineEdit)
            return input_element

    def readPortfolioLineEdit(self) -> str:
        input_element = self.window.portfolio_comboBox.currentText()
        print(input_element)
        if input_element in "":
            self.setErrorColor(self.window.input_lineEdit)
        else:
            self.resetErrorColor(self.window.input_lineEdit)
            return input_element

    @staticmethod
    def setErrorColor(element) -> None:
        """
        It sets the background color of the element to red
        
        :param element: The element to set the color of
        """
        element.setStyleSheet("background-color:rgb(250,0,0);")

    @staticmethod
    def resetErrorColor(element) -> None:
        """
        It takes an element as an argument and sets the background color of that element to black
        
        :param element: The element to change the color of
        """
        element.setStyleSheet('background-color:rgb(0,0,0);')
