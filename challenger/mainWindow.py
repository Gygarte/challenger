import logging
import json
import time
from typing import List, Union
import pandas as pd
import os
from pathlib import Path
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThreadPool
from challenger.gui.mainWindow import Ui_MainWindow
# TODO: Setarile privind numele documentelor de input, ar trebui sa fie salvate automat intr-un fisier de configuratie
from challenger.logger_setup import setup_logger
from challenger.excel_saver import save_to_excel
from challenger.ExecuteSteps import ExecuteSteps
from challenger.resource_path import resource_path
from challenger.Workers import ProcessingWorker, SaverWorker, ExecutorWorker
from challenger.Preprocessor import Preprocessor


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
        self.window.select_output_path_checkBox.toggled.connect(lambda: self.setOutputFolderPath())

        # display default values from setting into corresponding fields
        self.loadInitialSetup()

        # set some text to progress bar
        self.window.progress.setValue(0)
        self.window.progress.setFormat("Ready!")
        self.window.progress.setAlignment(QtCore.Qt.AlignCenter)

        # connect to ExecuteSteps class to run the backend
        self.execute_algo = ExecuteSteps()
        # self.execute_algo.currentModel.connect(self.updateProgressBar)
        # self.execute_algo.currentState.connect(self.updateProgressBarWithName)

        # update the output field with the name of the output file based on portfolio name
        self.window.portfolio_name.currentIndexChanged.connect(lambda: self.setOutputFileName())
        # logging
        self._log = setup_logger("out", os.path.join(Path(__file__).resolve(True).parent, "out.log"))

        # threading
        self.threadpool = QThreadPool()

    _initial_setup_file_path = resource_path("basic_setup.json")

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

        portfolio_sheet_name = self.readPortfolioLineEdit()
        macro_sheet_name = self.readMacroSheetLineEdit()
        data_sheet_name = self.readDataSheetLineEdit()
        input_file_name = self.readInputFileNameLineEdit()
        number_of_variables = self.readNumberOfVariablesLineEdit()
        sign_dict = self.readSignTable()

        print(number_of_variables)
        self._log.info(f"""Path to input: {path_to_input_folder}
              Portfolio: {portfolio_sheet_name}
              Sign_dict: {sign_dict}
              Input file name: {input_file_name}
              Data sheet name: {data_sheet_name}
              Macro Sheet name: {macro_sheet_name}
              Number of variables: {number_of_variables}
              """)

        # TODO:Make an exception window for when you press RUN by mistake
        self.execute_algo.set_log = self._log

        preprocessor = Preprocessor(path_to_input_folder,
                                    input_file_name,
                                    portfolio_sheet_name,
                                    macro_sheet_name,
                                    data_sheet_name,
                                    number_of_variables[0],
                                    sign_dict)
        preprocessor.set_log = self._log
        instructions, output_template, data = preprocessor.run_preprocess()
        print(f"The len of instructions is {len(instructions)}")

        executor_worker = ExecutorWorker(self._log, instructions, data)
        executor_worker.signals.result.connect(self.printResult)
        executor_worker.signals.start.connect(self.printStart)

        """
        self._call_return = self.execute_algo.execute_challenger(path_to_input_folder,
                                                                 input_file_name,
                                                                 portfolio_sheet_name,
                                                                 macro_sheet_name,
                                                                 data_sheet_name,
                                                                 number_of_variables,
                                                                 sign_dict)
        print(self._call_return)
        """
        # Execute

        self.threadpool.start(executor_worker)

    def printStart(self):
        print("Start Work!")

    def setCallReturn(self, obj) -> None:
        self._call_return = obj

    def callSaveFunction(self) -> None:
        # TODO: Create a popup to raise attention when trying to save an unexisting file, or the path is not specified
        if self._call_return is None:
            self._log.info("Attempt to save a file that does not exists!")
            return None

        if self.readOutputFolderLineEdit() is None:
            self._log.info("Attempt to save a file to an unspecified location!")
            return None

        if self.window.select_output_path_checkBox.isChecked():
            path_to_output_folder = self.readInputFolderLineEdit()
        else:
            path_to_output_folder = self.readOutputFolderLineEdit()

        output_name = self.readOutputNameLineEdit()

        self._log.info("Pat to save: {}, name to save: {}".format(path_to_output_folder, output_name))

        save_worker = SaverWorker(save_to_excel,
                                  self._call_return,
                                  path_to_output_folder,
                                  output_name)
        save_worker.signals.finished.connect(self.displayFinished)

        self.threadpool.start(save_worker)

    def callSelectInputFolderDialog(self) -> None:
        """
        It opens a file dialog and sets the text of a lineEdit widget to the path of the selected
        directory
        """
        input_directory_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Input Directory')

        self._log = setup_logger("project_log", os.path.join(input_directory_path, "project_log.log"))

        input_sheets = readInputFileSheets(input_directory_path, self._log, self.window.input_file_name.text())

        self.window.portfolio_name.addItems(input_sheets)

        self.window.input_lineEdit.setText(input_directory_path)

        QtWidgets.QApplication.processEvents()

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
        input_element = self.window.portfolio_name.currentText()
        print(input_element)
        if input_element in "":
            self.setErrorColor(self.window.input_lineEdit)
        else:
            self.resetErrorColor(self.window.input_lineEdit)
            return input_element

    def readMacroSheetLineEdit(self) -> str:
        return self.window.macro_sheet_name.text()

    def readDataSheetLineEdit(self) -> str:
        return self.window.data_sheet_name.text()

    def readInputFileNameLineEdit(self) -> str:
        return self.window.input_file_name.text()

    def readOutputNameLineEdit(self) -> str:

        return self.window.output_file_name.text()

    def readNumberOfVariablesLineEdit(self) -> list:
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

    def readSignTable(self) -> dict:
        sign_dict = {}
        for row_index in range(self.window.sign_table.rowCount()):
            variable = self.window.sign_table.item(row_index, 0).text()
            sign = int(self.window.sign_table.item(row_index, 1).text())

            sign_dict.update({variable: sign})
        return sign_dict

    def updateProgressBar(self, value) -> None:
        self.window.progress.setValue(value)
        self.window.progress.setFormat(str(value) + "%")

        if value == 100:
            self.window.progress.setFormat("Done! Ready to be saved!")
        QtWidgets.QApplication.processEvents()

    def updateProgressBarWithName(self, value) -> None:
        self.window.label.setText(value)

    def loadInitialSetup(self) -> None:
        with open(self._initial_setup_file_path, "r") as file:
            setup_data = json.load(file)

            self.window.macro_sheet_name.setText(setup_data.get("macro_sheet_name"))
            self.window.data_sheet_name.setText(setup_data.get("data_sheet_name"))
            self.window.input_file_name.setText(setup_data.get("input_file_name"))

    def loadProjectSetup(self, path) -> None:
        with open(path, "r") as file:
            setup_data = json.load(file)

            self.window.macro_sheet_name.setText(setup_data.get("macro_sheet_name"))
            self.window.data_sheet_name.setText(setup_data.get("data_sheet_name"))
            self.window.input_file_name.setText(setup_data.get("input_file_name"))
            self.loadProjectSignDict()

    def loadProjectSignDict(self):
        # implement the loading of a saved dictionary from an existing project
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

    @staticmethod
    def printResult(value):
        print(f"Total time for task was {value}")

    def displayFinished(self):
        self.window.progress.setFormat("Saved!")
        QtWidgets.QApplication.processEvents()

    def setOutputFolderPath(self):
        path = self.window.input_lineEdit.text()
        self.window.output_lineEdit.setText(path)

    def setOutputFileName(self):
        text = self.window.portfolio_name.currentText() + "_" + time.strftime("%d-%m-20%y-%H-%M-%S",
                                                                              time.localtime()) + ".xlsx"
        self.window.output_file_name.setText(text)
