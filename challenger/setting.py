import time

"""
@@@ The setup file contains al informations about the process and suport files @@@

@INPUT:
    DOC           - Required : the name of the database containing the stationary variables (str)
    PORTFOLIO     - Required : the name of the sheet from DOC that is modelled              (str)
    DATABASE      - Required : the name of the database used                                (str)
"""
t = time.localtime()
t_format = time.strftime("%d-%m-20%y", t)


DOC = "Rezultate teste stationaritate.xlsx"
PORTFOLIO = "ALL"
DATABASE = "input.xlsx"
OUTPUT = "output" + "_" + PORTFOLIO + "_" + t_format + ".xlsx" 
