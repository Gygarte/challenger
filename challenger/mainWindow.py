import logging
import json
from typing import List, Union
import pandas as pd
import os
from pathlib import Path
from PyQt5 import QtWidgets
from challenger.gui.mainWindow import Ui_MainWindow
# TODO: Setarile privind numele documentelor de input, ar trebui sa fie salvate automat intr-un fisier de configuratie
from challenger.logger_setup import setup_logger
from challenger.excel_saver import save_to_excel
from challenger.ExecuteSteps import ExecuteSteps
from challenger.resource_path import resource_path

def readInputFileSheets(path_to_directory: Union[Path, str], _log: logging.log, doc: str) -> List[str]:
    try:
        _log.info("The path to input directory is: {}".format(path_to_directory))
        df = pd.ExcelFile(os.path.join(path_to_directory, doc))
        return df.sheet_names
    except (FileNotFoundError, ValueError):
        return ["No sheet!"]


# It creates a class called MainWindow that inherits from QMainWindow.
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None) -> None:
        QtWidgets.QMainWindow.__init__(self)
        self.window = Ui_MainWindow()
        self.window.setupUi(self)

        self._call_return = None

        self.window.exit_botton.clicked.connect(lambda: self.close())
        self.window.add_botton.clicked.connect(lambda: self.addSignToDict())
        self.window.delete_botton.clicked.connect(lambda: self.deleteSignFromDict())
        self.window.run_botton.clicked.connect(lambda: self.callRunFunction())
        self.window.save_botton.clicked.connect(lambda: self.callSaveFunction())
        self.window.select_input_path_button.clicked.connect(lambda: self.callSelectInputFolderDialog())

        # display default values from setting into corresponding fields
        self.loadInitialSetup()
        # self.window.doc_lineEdit.setText(DOC)
        # self.window.database_lineEdit.setText(DATABASE)
        # self.window.output_name_lineEdit.setText(OUTPUT)

        # connect to ExecuteSteps class to run the backend
        self.execute_algo = ExecuteSteps()
        self.execute_algo.currentModel.connect(self.updateProgressBar)

        # logging
        self._log = setup_logger("out", os.path.join(Path(__file__).resolve(True).parent, "out.log"))

    _initial_setup_file_path = resource_path("challenger/basic_setup.json")

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
        path_to_input_folder = self.readInputFolderLineEdit()

        portfolio = self.readPortfolioLineEdit()
        sign_dict = self.readSignTable()
        # TODO: make the stationary_document name changeable
        stationary_document = self.readStationaryDocumentLineEdit()
        input_database = self.readInputDatabaseLineEdit()
        treshold = self.readNumberOfVariablesLineEdit()
        stop_filter = self.window.only_varaibles_checkBox.isChecked()

        self._log.info("""Path to input: {}
              Portfolio: {}
              Sign_dict: {}
              Stationarity: {}
              Input Database: {}
              Treshold: {}
              Stop Filter: {}""".format(path_to_input_folder, portfolio, sign_dict, stationary_document,
                                        input_database, treshold, stop_filter))

        # TODO:Make an exception window for when you press RUN by mistake
        self.execute_algo.set_log = self._log
        self._call_return = self.execute_algo.main(path_to_input_folder, stationary_document, portfolio, input_database,
                                                   sign_dict, treshold, stop_filter)

    def callSaveFunction(self) -> None:
        # TODO: Create a popup to raise attention when trying to save an unexisting file, or the path is not specified
        if self._call_return is None:
            self._log.info("Attempt to save a file that does not exists!")

        if self.readOutputFolderLineEdit() is None:
            self._log.info("Attempt to save a file to an unspecified location!")
            return None

        if self.window.select_output_path_checkBox.isChecked():
            path_to_output_folder = self.readInputFolderLineEdit()
        else:
            path_to_output_folder = self.readOutputFolderLineEdit()

        output_name = self.readOutputNameLineEdit()

        self._log.info("Pat to save: {}, name to save: {}".format(path_to_output_folder, output_name))

        save_to_excel(self._call_return, path_to_output_folder, output_name)

    def callSelectInputFolderDialog(self) -> None:
        """
        It opens a file dialog and sets the text of a lineEdit widget to the path of the selected
        directory
        """
        input_directory_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Input Directory')

        self._log = setup_logger("project_log", os.path.join(input_directory_path, "project_log.log"))

        input_sheets = readInputFileSheets(input_directory_path, self._log, self.window.doc_lineEdit.text())

        self.window.portfolio_comboBox.addItems(input_sheets)

        self.window.input_lineEdit.setText(input_directory_path)

    def readInputFolderLineEdit(self) -> Path:
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
            return Path(input_element).resolve(True)

    def readOutputFolderLineEdit(self) -> Path:
        input_element = self.window.output_lineEdit.text()

        if input_element in "":
            self.setErrorColor(self.window.input_lineEdit)
        else:
            self.resetErrorColor(self.window.input_lineEdit)
            return Path(input_element).resolve(True)

    def readPortfolioLineEdit(self) -> str:
        input_element = self.window.portfolio_comboBox.currentText()
        print(input_element)
        if input_element in "":
            self.setErrorColor(self.window.input_lineEdit)
        else:
            self.resetErrorColor(self.window.input_lineEdit)
            return input_element

    def readSignTable(self) -> dict:
        sign_dict = {}
        for row_index in range(self.window.sign_table.rowCount()):
            variable = self.window.sign_table.item(row_index, 0).text()
            sign = int(self.window.sign_table.item(row_index, 1).text())

            sign_dict.update({variable: sign})
        return sign_dict

    def readStationaryDocumentLineEdit(self) -> str:
        return self.window.doc_lineEdit.text()

    def readInputDatabaseLineEdit(self) -> str:
        return self.window.database_lineEdit.text()

    def readNumberOfVariablesLineEdit(self) -> float:
        value_field = self.window.model_variables_lineEdit.text()
        if value_field in "":
            return 2
        else:
            return int(value_field)

    def readOutputNameLineEdit(self) -> str:
        return self.window.output_name_lineEdit.text()

    def updateProgressBar(self, value) -> None:
        self.window.progress.setValue(value)
        QtWidgets.QApplication.processEvents()

    def loadInitialSetup(self) -> None:
        with open(self._initial_setup_file_path, "r") as file:
            setup_data = json.load(file)

            self.window.doc_lineEdit.setText(setup_data.get("DOC"))
            self.window.database_lineEdit.setText(setup_data.get("DATABASE"))
            self.window.output_name_lineEdit.setText(setup_data.get("OUTPUT"))

    def loadProjectSetup(self, path) -> None:
        with open(path, "r") as file:
            setup_data = json.load(file)

            self.window.doc_lineEdit.setText(setup_data.get("DOC"))
            self.window.database_lineEdit.setText(setup_data.get("DATABASE"))
            self.window.output_name_lineEdit.setText(setup_data.get("OUTPUT"))
            self.loadProjectSignDict()

    def loadProjectSignDict(self):
        #implement the loading of a saved dictionary from an existing project
        pass

    @staticmethod
    def saveProjectSetup(path, data) -> None:
        """

        :param path:
        :param data:
        :return:
        """
        with open(path, "w") as file:
            json.dump(data, file, indent=4)

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
        element.setStyleSheet('background-color:rgb(255,255,255);')
