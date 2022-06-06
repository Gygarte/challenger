from challenger_v2 import main

""" 
@@@ Challenger script verison 2  @@@

This script is ment to offer a reliable way of building challenger models from a pool of varibles.

It accepts as inputs dependent variables from a file named "Rezultate teste stationaritate.xls". Each
sheet coresponds to a portfolio. The time seris coresponding to the said dependent variables are took
from a file names "input.xlsx", sheet "input". 

The independent variables are took from the "input.xlsx" sheet "macro". It is necessary that all macro 
vartiables to be stationary. Auto-selection of stationary macro variables will be implemented later.

The output consists of file "output.xlsx" containing 2 sheets for each type of model built.
 

"""

if __name__ == "__main__":
    main()
