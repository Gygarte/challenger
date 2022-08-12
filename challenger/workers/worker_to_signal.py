from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal


class WorkerSignals(QObject):
    """
    Used signals:

    finished: No data
    error: tuple (exctype, value, traceback.format_exc())
    result: object data => Pandas DataFrame
    progress: int - returned from main processing class


    """
    finished = pyqtSignal(str)
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class SaveWorkerSignals(WorkerSignals):
    pass


class PreprocessingWorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)


class ExecutorWorkerSignals(QObject):
    start = pyqtSignal()
    finished = pyqtSignal()
    status = pyqtSignal(int)
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
