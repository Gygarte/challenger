import traceback
import sys
import time
import pandas as pd
from PyQt5.QtCore import QRunnable
from challenger.workers import worker_to_signal
from challenger.old import compute_models
from typing import Generator
import multiprocessing as mp


class ExecutorWorker(QRunnable):
    """Implement the process that handles the execution of the algorithm"""

    def __init__(self, generator: Generator, number_of_instructions: int) -> None:
        super(QRunnable, self).__init__()
        self._generator = generator
        self._number_of_instructions = number_of_instructions
        self.signals = worker_to_signal.WorkerSignals()

    def run(self):
        try:

            t0: float = time.perf_counter()
            number_of_executors = int(mp.cpu_count() / 2)
            pool = mp.Pool(number_of_executors,
                           maxtasksperchild=1000)

            result = pool.map_async(func=compute_models.compute_models_modified2,
                                    iterable=self._generator(),
                                    chunksize=250)

            t1 = time.perf_counter()
            print(f"Elapsed time is {t1 - t0} seconds, or {((t1 - t0) / 60 )} minutes")

            # cleaning
            pool.close()
            pool.join()

            print("Results compiled...")
            self.signals.result.emit(result.get())

        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit("Finished to compile!")
