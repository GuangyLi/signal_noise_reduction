# Python function to adjust different data of same type to same length
# Also automatically alignment the data which suppose to be the similiar signal

import sys
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    from file_load import FileIn
else:
    from lib.file_load import FileIn

# Rising and Falling edge, control with current

# Funtion that aligns file in files close to same start point
# neglect_pulse_width for maximum pulse width that is igrnored as noise
def auto_align(files, edge = "rising", tvalue="auto", neglect_pulse_width=1, skip_steps=1, input_edges="None"):
    # Error handling
    if not isinstance(files, list):
        raise TypeError("Sorry. 'files' must be list.")
    if not all(isinstance(f, FileIn) for f in files):
        raise TypeError("Sorry. items in 'files' must be FileIn type.")
    
    # Allow input known edges to manually align data
    if input_edges != "None":
        if not isinstance(input_edges, list):
            raise TypeError("Sorry. 'input_edges' must be a list.")
        if not all(isinstance(e, int) for e in input_edges):
            raise TypeError("Sorry. items in 'input_edges' must be int type.")
        if not (len(input_edges) == len(files)):
            raise TypeError("Sorry. length of 'input_edges' must be same as length of 'files'.")    
    
    # Rising edge triggered or falling edge triggered, default to rising
    if (edge != "rising") and (edge != "falling"):
        raise TypeError("Sorry. 'edge' must be either rising or falling.")
    
    # Triggered at which value, default to automatic generation
    if tvalue != "auto":
        if not isinstance(tvalue, int):
            raise TypeError("Sorry. 'tvalue' must be an integer.")
        if not tvalue >= 0:
            print("WARNING. 'tvalue' should be positive for most cases.")
    
    # Ensureneglect_pulse_width to be positive int
    if not isinstance(neglect_pulse_width, int):
        raise TypeError("Sorry. 'neglect_pulse_width' must be int.")
    if not neglect_pulse_width >= 1:
        print("WARNING. 'neglect_pulse_width' must be larger than or equal to 1.")
        
    # skip_steps to be positive int
    if not isinstance(skip_steps, int):
        raise TypeError("Sorry. 'skip_steps' must be int.")
    if not skip_steps >= 1:
        print("WARNING. 'skip_steps' must be larger than or equal to 1.")
    
    file_num = len(files)
    
    first_edges = []
    valid_edges = []
    invalid_edges = []
    if input_edges == "None":
        for f in files:
            cur_max = f.get_max()
            cur_min = f.get_min()
            if tvalue == "auto":
                edge_val = int((cur_max+cur_min)/2)
            else:
                edge_val = tvalue
            cur_fe = find_first_edge(f, "rising", edge_val, neglect_pulse_width, skip_steps)
            first_edges.append(cur_fe)
            
            if cur_fe != -1: valid_edges.append(cur_fe)
            
        earliest_edge = min(valid_edges)
        avg_edge = int(sum(first_edges)/file_num)
        print("Earliest edge is: %d, and average edge is: %d." %(earliest_edge, avg_edge))
        
        # Optimize the first edges, remove -1 and other unrecognized ones
        for i in range(file_num):
            print("%s original first edge is %d." %(files[i].file_name, first_edges[i]))
            
            if ( (first_edges[i] == -1) or (first_edges[i] >= 5*earliest_edge or abs(first_edges[i]-avg_edge) >= 300) ):
                first_edges[i] = avg_edge
                invalid_edges.append(i)
                
            print("%s later first edge is %d." %(files[i].file_name, first_edges[i]))
    else:
        first_edges = list(input_edges)
        earliest_edge = min(first_edges)
    
    # Align all the data
    for i in range(file_num):
        if first_edges[i] > earliest_edge:
            edge_diff = first_edges[i] - earliest_edge
            cur_data = files[i].data
            data_len = len(cur_data)
            di = edge_diff
            while(di < data_len):
                cur_data[di-edge_diff] = cur_data[di]
                di += 1
            
            files[i].data = cur_data[:-edge_diff]
        files[i].aligned = True
    
    # Adjust the files after alignment
    auto_adjust(files)
    
    return first_edges, invalid_edges

# Funtion that adjust file in files to same length
def auto_adjust(files):
    # Error handling
    if not isinstance(files, list):
        raise TypeError("Sorry. 'files' must be list.")
    if not all(isinstance(f, FileIn) for f in files):
        raise TypeError("Sorry. items in 'files' must be FileIn type.")
    
    # Find the minimum size in files
    min_size = float("inf")
    for f in files:
        cur_dsize = f.get_data_size()
        if cur_dsize < min_size:
            min_size = cur_dsize
    
    # Reduce all data in files to min_size
    for f in files:
        f.data = f.data[:min_size]
        f.adjusted = True
    
    return

# Function that find the first rising/falling edge
def find_first_edge(file, edge, tvalue, min_pw, skip_steps):
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
            
    # min_pw to be positive int
    if not isinstance(min_pw, int):
        raise TypeError("Sorry. 'min_pw' must be int.")
    if not min_pw >= 1:
        print("WARNING. 'min_pw' must be larger than or equal to 1.")
        
    # skip_steps to be positive int
    if not isinstance(skip_steps, int):
        raise TypeError("Sorry. 'skip_steps' must be int.")
    if not skip_steps >= 1:
        print("WARNING. 'skip_steps' must be larger than or equal to 1.")
            
    temp_data = file.data
    data_len = len(temp_data)
    pivot = min_pw*skip_steps
    first_edge = -1
    
    # Check points before and after the pivot tp find out the first edge
    while (pivot < data_len - (min_pw * skip_steps)):
        start_point = pivot - (min_pw * skip_steps)
        end_point = pivot + (min_pw * skip_steps)
        is_edge = 1
        for i in range(min_pw):
            next_p = i * skip_steps
            if edge == "rising":
                #if (temp_data[start_point+next_p] > tvalue*0.9) or (temp_data[end_point-next_p] < tvalue*1.1):
                if (temp_data[end_point-next_p] < tvalue*1.1):
                    is_edge = 0
            else:
                if (temp_data[start_point+next_p] < tvalue*0.9) or (temp_data[end_point-next_p] > tvalue*1.1):
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
    use_google = 0
    if use_google:
        test1 = FileIn("data/google3.txt", 334, 167)
        test2 = FileIn("data/google4.txt", 334, 167)
    else:
        test1 = FileIn("data/temp1.txt", 334, 167)
        test2 = FileIn("data/temp2.txt", 334, 167)

    test_files = [test1, test2]
    auto_align(test_files, neglect_pulse_width=2, skip_steps=1, input_edges="None")
    
    if (test1.adjusted and test1.aligned and test2.adjusted and test2.aligned):
        print("All adjusted and aligned")
    
    # Plot data to verify the alignment
    fig, ax = plt.subplots(figsize=(20,4))
    ax.plot(test1.data, c='b', label='temp1')
    ax.plot(test2.data, c='r', label='temp2')
    
    plt.legend(loc='best');
    plt.show()    
    print("--------Verification ends--------\n")