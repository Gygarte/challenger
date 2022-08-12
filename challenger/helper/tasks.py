import queue
from multiprocessing import Process
from multiprocessing import JoinableQueue, Queue
from challenger.algo import compute_models
import traceback
import sys
import pandas as pd


class Executor(Process):
    def __init__(self, task_queue: JoinableQueue, result_queus: Queue,
                 error_queue: Queue, supervisor_queue: Queue(), data: pd.DataFrame) -> None:
        super(Process, self).__init__()
        self._task_queue = task_queue
        self._result_queue = result_queus
        self._error_queue = error_queue
        self._data = data
        self._supervisor_queue = supervisor_queue


    def run(self) -> None:
        try:
            while True:
                next_task = self._task_queue.get()
                if next_task is None:
                    break
                result = next_task(self._data)
                self._task_queue.task_done()
                self._result_queue.put(result)
                self._supervisor_queue.put(1)
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self._error_queue.put((exctype, value, traceback.format_exc()))
            self.terminate()


class Supervisor(Process):
    def __init__(self, supervisor_queue: Queue) -> None:
        super(Process, self).__init__()
        self._supervisor_queue = supervisor_queue
        self.daemon = True

    def run(self) -> None:
        try:
            message = self._supervisor_queue.get(timeout=3)
        except queue.Empty as empty:
            self._supervisor_queue.put(None)


class Task:
    def __init__(self, data_in: tuple) -> None:
        self._data_in = data_in

    def __call__(self, data: pd.DataFrame) -> list:
        result = compute_models.compute_models_modified(self._data_in, data)
        return result
