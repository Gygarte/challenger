from abc import ABC, abstractmethod
from PyQt5.QtCore import QThreadPool, QRunnable
from preprocessor import Preprocessor
from challenger.workers.worker_to_execute_algo import ExecutorWorker
from PyQt5.QtCore import QObject, pyqtSignal

from typing import List

class Algorithm_SignalTransporter(QObject):
    transporter_finished = pyqtSignal(bool)
    transporter_error = pyqtSignal(tuple)
    transporter_result = pyqtSignal(object)
    transporter_progress = pyqtSignal(float)


class Algorithm(ABC):
    @abstractmethod
    def run(self):
        """
        To run the worker responsable for calculating the models

        """

    @abstractmethod
    def prepare_to_save(self):
        """
        To take the outputs and prepare for saving
        """

    @abstractmethod
    def save(self):
        """
        To save the final output ot a file
        """


class Algorithm_Handler(Algorithm):
    def __init__(self, thread_pool: QThreadPool, worker_to_preprocess: QRunnable,
                 worker_to_execute_algo: QRunnable, worker_to_save: QRunnable):
        self._thread_pool = thread_pool
        self._worker_to_preprocess = worker_to_preprocess
        self._worker_to_execute_algo = worker_to_execute_algo
        self._worker_to_save = worker_to_save

        # transport
        self.signals = Algorithm_SignalTransporter()
        self._result = None

    def run(self, data_input: dict, worker_to_execute_algo: ExecutorWorker) -> None:
        preprocessor = Preprocessor(data_input)
        data_in, output_template, data = preprocessor.run()
        worker_to_execute_algo.set_data_in(data_in)
        worker_to_execute_algo.set_data(data)


        self.signals.transporter_error.emit(worker_to_execute_algo.signals.error)
        self.signals.transporter_finished.emit(worker_to_execute_algo.signals.finished)
        self.signals.transporter_progress.emit(worker_to_execute_algo.signals.progress)
        self._result = worker_to_execute_algo.signals.result

        self._thread_pool.start(worker_to_execute_algo)
    def prepare_to_save(self):
        ...

    def save(self):
        ...

    def default_safe(self):
        ...

    def set_thread_pool(self, thread_pool):
        self._thread_pool = thread_pool

    def set_worker_to_preprocess(self, preprocessor_worker):
        self._worker_to_preprocess = preprocessor_worker

    def set_worker_to_execute_algo(self, executor_worker):
        self._worker_to_execute_algo = executor_worker

    def set_worker_to_save(self, saver_worker):
        self._worker_to_save = saver_worker

    def _batching(self, data_in: list) -> List[list]:
        """
        To limit the limit the data that are fed to the processing pool

        """
        LIMIT = 10000

        if len(data_in > 10000):
            pass