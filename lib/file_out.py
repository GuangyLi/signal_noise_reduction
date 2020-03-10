# Python function to store generated data in a file with corresponding heading and value in each line

import sys
import numpy as np
from file_load import FileIn

def file_out(file):
    # Error handling
    if not isinstance(file, FileIn):
        raise TypeError("Sorry. 'file' must be FileIn type.")
    
    return

if __name__ == "__main__":
    # Functional level verification starts here
    print("--------File out functional verification--------\n")
    test = FileIn("data/google1.txt", 334)
    file_out(test)
    print("--------Verification ends--------\n")