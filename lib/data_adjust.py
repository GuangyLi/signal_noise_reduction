# Python function to adjust different data of same type to same length
# Also automatically alignment the data which suppose to be the similiar signal

import sys
import numpy as np
#from lib.file_load import FileIn
from file_load import FileIn
import matplotlib.pyplot as plt

############################
############TBD#############
############################
# Rising and Falling edge, control with current

# Funtion that aligns file in files close to same start point
def auto_align(files, edge = "rising", value="auto"):
    # Error handling
    if not isinstance(files, list):
        raise TypeError("Sorry. 'files' must be list.")
    if not isinstance(files[0], FileIn):
        raise TypeError("Sorry. items in 'files' must be FileIn type.")    
    
    
    
    auto_adjust(files)
    
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
    data1 = np.array([1,1,2,1,2,1,1,5,7,5,6,2,1,1,1,2,1,1,1,2,1])
    data2 = np.array([3,2,2,2,3,3,2,2,2,6,8,6,7,2,2,3,2])
    test1 = FileIn("data/temp1.txt", 334, 167)
    test2 = FileIn("data/temp2.txt", 334, 167)
    test_files = [test1, test2]
    auto_align(test_files)
    
    # Plot data to verify the alignment
    fig, ax = plt.subplots(figsize=(20,4))
    ax.plot(test1.data, c='b', label='temp1')
    ax.plot(test2.data, c='r', label='temp2')
    
    plt.legend(loc='best');
    plt.show()    
    print("--------Verification ends--------\n")