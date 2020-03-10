# Python function to adjust different data of same type to same length
# Also automatically alignment the data which suppose to be the similiar signal

import sys
import numpy as np
from file_load import FileIn

# Funtion that aligns file in files close to same start point
def auto_align(files):
    # Error handling
    if not isinstance(files, list):
        raise TypeError("Sorry. 'files' must be list.")
    if not isinstance(files[0], FileIn):
        raise TypeError("Sorry. items in 'files' must be FileIn type.")    
    
    return

# Funtion that adjust file in files to same length
def auto_adjust(files):
    # Error handling
    if not isinstance(files, list):
        raise TypeError("Sorry. 'files' must be list.")
    if not isinstance(files[0], FileIn):
        raise TypeError("Sorry. items in 'files' must be FileIn type.")    
    
    return

if __name__ == "__main__":
    # Functional level verification starts here
    print("--------File out functional verification--------\n")
    test1 = FileIn("data/google1.txt", 334)
    test2 = FileIn("data/google2.txt", 334)
    test_files = [test1, test2]
    auto_align(test_files)
    auto_adjust(test_files)
    print("--------Verification ends--------\n")