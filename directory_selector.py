from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory

"""

@@@ Calls a window for selecting the directory in which the database is situated @@@

@OUTPUT:
    filepath : the apth to the directory in which the database is situated

"""


def directory_selector_dialog() -> str:
    """
    It opens a dialog box that allows you to select a directory
    :return: The filepath of the directory selected by the user.
    """
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filepath = askdirectory() # show an "Open" dialog box and return the path to the selected file

    #formating the filename
    filepath = filepath + "/"

    return(filepath)