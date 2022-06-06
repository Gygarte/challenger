import time

"""
@@@ The setup file contains al informations about the process and suport files @@@

@INPUT:
    DOC           - Required : the name of the database containing the stationary variables (str)
    PORTFOLIO     - Required : the name of the sheet from DOC that is modelled              (str)
    DATABASE      - Required : the name of the database used                                (str)
    TRESHOLD      - Required : the level at which the variables are considered correlated   (float)
    STOP_FILTER   - Required : neccessary if the correlation filter is considered           (bool)
    OUTPUT        - Auto     : auto generated naem of the output file                       (str)

"""
t = time.localtime()
t_format = time.strftime("%d-%m-20%y", t)


DOC = "Rezultate teste stationaritate.xlsx" #trebuie facute modificari la baza de date
PORTFOLIO = "ALL" #de 
DATABASE = "input.xlsx"
OUTPUT = "output" + "_" + PORTFOLIO + "_" + t_format + ".xlsx" 
TRESHOLD = 0.001
STOP_FILTER = True
SIGN_DICT = {"GDP": -1, "CPI":+1, "UR":+1, "ROBOR":+1}

#__all__ = [DOC, PORTFOLIO, DATABASE, OUTPUT]