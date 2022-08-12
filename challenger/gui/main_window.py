import os
import json
from pathlib import Path
from challenger.gui.main_window_gui_functions import MainWindow_GUI_Functions
from challenger.gui.main_window_gui_template import Ui_MainWindow
from challenger.resource_path import resource_path
from challenger.helper.algorithm_handler import Algorithm
from PyQt5 import QtCore
from PyQt5.QtCore import QThreadPool
from challenger.logger_setup import setup_logger


class MainWindow(MainWindow_GUI_Functions):
    def __init__(self, algorithm_handler: Algorithm) -> None:
        MainWindow_GUI_Functions.__init__(self, Ui_MainWindow())
        """Initial setup should be a script in the class that will inherit this one"""
        # display default values from setting into corresponding fields
        self.loadInitialSetup()

        # set some text to progress bar
        self.window.progress.setValue(0)
        self.window.progress.setFormat("Ready!")
        self.window.progress.setAlignment(QtCore.Qt.AlignCenter)

        # update the output field with the name of the output file based on portfolio name
        self.window.portfolio_name.currentIndexChanged.connect(lambda: self._setOutputFileName())
        # logging
        self._log = setup_logger("out", os.path.join(Path(__file__).resolve(True).parent, "out.log"))

        self._algorithm_handler = algorithm_handler

    _initial_setup_file_path = resource_path("basic_setup.json")

    def callRunFunction(self) -> None:
        pass

    def callSaveFunction(self) -> None:
        pass

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

    @staticmethod
    def saveProjectSetup(path, data) -> None:
        with open(path, "w") as file:
            json.dump(data, file, indent=4)

    def loadProjectSignDict(self):
        # implement the loading of a saved dictionary from an existing project
        pass

    @staticmethod
    def printResult(value):
        print(f"Total time for task was {value}")

    def displayFinished(self):
        self.window.progress.setFormat("Saved!")
        QtWidgets.QApplication.processEvents()
