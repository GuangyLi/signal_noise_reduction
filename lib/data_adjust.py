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
def auto_align(files, edge = "rising", tvalue="auto"):
    # Error handling
    if not isinstance(files, list):
        raise TypeError("Sorry. 'files' must be list.")
    if not isinstance(files[0], FileIn):
        raise TypeError("Sorry. items in 'files' must be FileIn type.")
    
    # Rising edge triggered or falling edge triggered, default to rising
    if (edge != "rising") and (edge != "falling"):
        raise TypeError("Sorry. 'edge' must be either rising or falling.")
    
    # Triggered at which value, default to automatic generation
    if tvalue != "auto":
        if not isinstance(tvalue, int):
            raise TypeError("Sorry. 'tvalue' must be an integer.")
        if not tvalue >= 0:
            print("WARNING. 'tvalue' should be positive for most cases.")
    
    for f in files:
        cur_fe = find_first_edge(f, "rising", int(f.average)+1, 2)
        print("avg is %d" %f.average)
        print("%s first edge is %d" %(f.file_name, cur_fe))
    
    # Adjust the files after alignment
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

# Function that find the first rising/falling edge
def find_first_edge(file, edge, tvalue, min_pw):
    # Error handling
    if not isinstance(file, FileIn):
        raise TypeError("Sorry. 'file' must be FileIn type.")
    
    # Rising edge triggered or falling edge triggered, default to rising
    if (edge != "rising") and (edge != "falling"):
        raise TypeError("Sorry. 'edge' must be either rising or falling.")
    
    # Triggered at which value, default to automatic generation
    if tvalue != "auto":
        if not isinstance(tvalue, int):
            raise TypeError("Sorry. 'tvalue' must be an integer.")
        if not tvalue >= 0:
            print("WARNING. 'tvalue' should be positive for most cases.")
            
    temp_data = file.data
    data_len = len(temp_data)
    pivot = min_pw
    first_edge = -1
    
    while (pivot < data_len-min_pw):
        start_point = pivot-min_pw
        end_point = pivot+min_pw
        is_edge = 1
        for i in range(min_pw):
            if edge == "rising":
                if (temp_data[start_point+i] > tvalue*0.8) or (temp_data[end_point-i] < tvalue*1.2):
                    is_edge = 0
            else:
                if (temp_data[start_point+i] < tvalue*0.8) or (temp_data[end_point-i] > tvalue*1.2):
                    is_edge = 0
        
        if is_edge:
            first_edge = pivot
            break
        
        pivot += 1
        
    return first_edge

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