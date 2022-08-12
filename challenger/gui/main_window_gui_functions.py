import os
import time
import pandas as pd
from pathlib import Path
from PyQt5 import QtWidgets
from challenger.gui.main_window_gui_template import Ui_MainWindow
from challenger.logger_setup import setup_logger
from typing import Union, List


def readInputFileSheets(path_to_directory: Union[Path, str], doc: str) -> List[str]:
    try:

        df = pd.ExcelFile(os.path.join(path_to_directory, doc))
        return df.sheet_names
    except (FileNotFoundError, ValueError):
        return ["No sheet!"]


class MainWindow_GUI_Functions(QtWidgets.QMainWindow):
    def __init__(self, window: Ui_MainWindow) -> None:
        QtWidgets.QMainWindow.__init__(self)
        self.window = window
        self.window.setupUi(self)

        # connect the buttons fo specific functions
        self.window.exit_botton.clicked.connect(lambda: self.close())
        self.window.add_botton.clicked.connect(lambda: self._addSignToDict())
        self.window.delete_botton.clicked.connect(lambda: self._deleteSignFromDict())
        self.window.run_botton.clicked.connect(lambda: self.callRunFunction())
        self.window.save_botton.clicked.connect(lambda: self.callSaveFunction())
        self.window.select_input_path_button.clicked.connect(lambda: self._callSelectInputFolderDialog())
        self.window.select_output_path_checkBox.toggled.connect(lambda: self._setOutputFolderPath())

    def callRunFunction(self) -> None:
        raise NotImplemented

    def callSaveFunction(self) -> None:
        raise NotImplemented

    def readFields(self) -> dict:

        form_data = {"path_to_input_folder": self._readInputFolderLineEdit(),
                     "portfolio_sheet_name": self._readPortfolioLineEdit(),
                     "macro_sheet_name": self._readMacroSheetLineEdit(),
                     "data_sheet_name": self._readDataSheetLineEdit(),
                     "input_file_name": self._readInputFileNameLineEdit(),
                     "number_of_variables": self._readNumberOfVariablesLineEdit(),
                     "sign_dict": self._readSignTable()
                     }

        return form_data

    def updateProgressBar(self, value) -> None:
        self.window.progress.setValue(value)
        self.window.progress.setFormat(str(value) + "%")

        if value == 100:
            self.window.progress.setFormat("Done! Ready to be saved!")
        QtWidgets.QApplication.processEvents()

    def updateProgressBarWithName(self, value) -> None:
        self.window.label.setText(value)

    def _addSignToDict(self) -> None:
        """
        It adds a row to a table widget.
        """
        row_count = self.window.sign_table.rowCount()
        self.window.sign_table.setRowCount(row_count + 1)
        self.window.sign_table.setColumnCount(2)
        self.window.sign_table.setHorizontalHeaderLabels(["Variable", "Sign"])

    def _deleteSignFromDict(self) -> None:
        """
        It deletes the selected row from the table
        """
        row_number = self.window.sign_table.currentRow()
        self.window.sign_table.removeRow(row_number)

    def _callSelectInputFolderDialog(self) -> None:
        """
        It opens a file dialog and sets the text of a lineEdit widget to the path of the selected
        directory
        """
        input_directory_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Input Directory')

        self._log = setup_logger("project_log", os.path.join(input_directory_path, "project_log.log"))

        input_sheets = readInputFileSheets(input_directory_path, self.window.input_file_name.text())

        self.window.portfolio_name.addItems(input_sheets)

        self.window.input_lineEdit.setText(input_directory_path)

        QtWidgets.QApplication.processEvents()

    def _readInputFolderLineEdit(self) -> Path:
        """
        If the input_lineEdit is empty, set the error color, otherwise reset the error color and return
        the input_lineEdit text
        :return: The input_element is being returned.
        """
        input_element = self.window.input_lineEdit.text()

        if input_element in "":
            self._setErrorColor(self.window.input_lineEdit)
        else:
            self.resetErrorColor(self.window.input_lineEdit)

            path = Path(input_element).resolve(True)
            return path

    def _readOutputFolderLineEdit(self) -> Path:
        input_element = self.window.output_lineEdit.text()

        if input_element in "":
            self._setErrorColor(self.window.input_lineEdit)
        else:
            self.resetErrorColor(self.window.input_lineEdit)
            return Path(input_element).resolve(True)

    def _readPortfolioLineEdit(self) -> str:
        input_element = self.window.portfolio_name.currentText()
        print(input_element)
        if input_element in "":
            self._setErrorColor(self.window.input_lineEdit)
        else:
            self.resetErrorColor(self.window.input_lineEdit)
            return input_element

    def _readMacroSheetLineEdit(self) -> str:
        return self.window.macro_sheet_name.text()

    def _readDataSheetLineEdit(self) -> str:
        return self.window.data_sheet_name.text()

    def _readInputFileNameLineEdit(self) -> str:
        return self.window.input_file_name.text()

    def _readOutputNameLineEdit(self) -> str:

        return self.window.output_file_name.text()

    def _readNumberOfVariablesLineEdit(self) -> list:
        # Default value is 2 => a list containing the value of 2 is returned
        # Otherwise a list of all inputted values is returned
        value_field = self.window.number_of_variables.text()
        if value_field in "":
            return list([2])
        else:
            values = []
            for value in value_field.split(","):
                values.append(int(value))
            return values

    def _readSignTable(self) -> dict:
        sign_dict = {}
        for row_index in range(self.window.sign_table.rowCount()):
            variable = self.window.sign_table.item(row_index, 0).text()
            sign = int(self.window.sign_table.item(row_index, 1).text())

            sign_dict.update({variable: sign})
        return sign_dict

    @staticmethod
    def _setErrorColor(element) -> None:

        element.setStyleSheet("background-color:rgb(250,0,0);")

    def _setOutputFolderPath(self):
        path = self.window.input_lineEdit.text()
        self.window.output_lineEdit.setText(path)

    def _setOutputFileName(self):
        text = self.window.portfolio_name.currentText() + "_" + time.strftime("%d-%m-20%y-%H-%M-%S",
                                                                              time.localtime()) + ".xlsx"
        self.window.output_file_name.setText(text)
