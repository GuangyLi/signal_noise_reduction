import time
import os
import os.path as ospath
import numpy as np
import matplotlib.pyplot as plt
#import noisereduce as nr
from lib.file_load import FileIn
from lib.func_avg import average_signal
from lib.func_pulse import remove_pulse
import lib.data_adjust as adj

# Global variable that contains all allowed color in matplotlib, use html hex string for greater range
COLORS = ['b','g','r','c','m','y','k','w']
FILECATEGORY = ['temp','google','music','omusic','youtube']

# Flag determine whether use auto method or not and which method to use
auto_avg = 0
plot_smooth = 1
plot_slope = 1
avg_steps = 8
file_num = 0

def user_in_ctrl():
    global auto_avg, plot_slope, plot_smooth, avg_steps
    prompt_text = "which noise reduction method to apply (step/slope): \n"
    user_in = input(prompt_text)
    if user_in == "slope":
        plot_slope = 1
    elif user_in == "step":
        plot_slope = 0
    else:
        print("Invalid method detected, choose step as default\n")
        plot_slope = 0

    if plot_slope == 0:
        prompt_text = "output smooth curve? (y/n): \n"
        user_in = input(prompt_text)
        if user_in == "y":
            plot_smooth = 1
        elif user_in == "n":
            plot_smooth = 0
        else:
            print("Invalid output detected, choose smooth as default\n")
            plot_smooth = 1

    prompt_text = "how many steps to average (auto/any int): \n"
    user_in = input(prompt_text)
    if user_in == "auto":
        auto_avg = 1
    else:
        try:
            auto_avg = 0
            avg_steps = int(user_in)
            print("%d steps to average\n" %avg_steps)
        except:
            print("Invalid steps detected, choose auto as default\n")
            auto_avg = 1
    
    return

def load_files(file_loc, file_cate, file_count, count_start = 1):
    global file_num
    
    # Error handling
    if not isinstance(file_loc, str):
        raise TypeError("Sorry. 'file_loc' must be string.")
    if not isinstance(file_cate, str):
        raise TypeError("Sorry. 'file_cate' must be string.")
    if not isinstance(file_num, int):
        raise TypeError("Sorry. 'file_num' must be int.")
    if not isinstance(file_count, int):
        raise TypeError("Sorry. 'file_count' must be int.")
    if not isinstance(count_start, int):
        raise TypeError("Sorry. 'count_start' must be int.")    
    
    if not os.path.exists(file_loc):
        print("Warning: Destion doesn't exist, %s created" %file_loc)
        os.mkdir(file_loc)
    
    # Check exist files
    ext_files = [f for f in os.listdir(file_loc) if ospath.isfile(ospath.join(file_loc, f))]
    ext_num = 0
    ext_names = []
    for ext_name in ext_files:
        if file_cate in ext_name:
            ext_num += 1
            ext_names.append(ext_name)
    
    if ext_num == 0:
        raise TypeError("Sorry. %s related files doesn't exist in %s." %(file_cate, file_loc))
    
    if ext_num > file_count:
        ext_num = file_count
        ext_names = []
        for i in range(file_count):
            tmp_name = file_cate + str(i+count_start) + ".txt"
            ext_names.append(tmp_name)
    
    file_num = ext_num
    files = []
    
    for n in ext_names:
        filename_full = file_loc + n
        files.append(FileIn(filename_full, 334, 167))
    
    return files

def get_reduced_files(files):
    # Error handling
    if not isinstance(files, list):
        raise TypeError("Sorry. 'files' must be list.")
    if not all(isinstance(f, FileIn) for f in files):
        raise TypeError("Sorry. items in 'files' must be FileIn type.")    
    
    tmp_reduced = []
    
    for f in files:
        tmp_test = average_signal(f)
        
        if auto_avg:
            if plot_slope:
                tmp_reduced.append(tmp_test.slope_average_data(steps="auto"))
            elif plot_smooth:
                tmp_reduced.append(tmp_test.slope_average_data(steps="auto", atype="smooth"))
            else:
                tmp_reduced.append(tmp_test.slope_average_data(steps="auto", atype="step"))
        else:
            if plot_slope:
                tmp_reduced.append(tmp_test.slope_average_data(steps=avg_steps))
            elif plot_smooth:
                tmp_reduced.append(tmp_test.slope_average_data(steps=avg_steps, atype="smooth"))
            else:
                tmp_reduced.append(tmp_test.slope_average_data(steps=avg_steps, atype="step"))
    
    return tmp_reduced

def plot_files(files):
    # Error handling
    if not isinstance(files, list):
        raise TypeError("Sorry. 'files' must be list.")
    if not all(isinstance(f, FileIn) for f in files):
        raise TypeError("Sorry. items in 'files' must be FileIn type.")
    
    if len(files) > len(COLORS):
        print("Warning: too many files might cause unrecognized output")
    
    fig, ax = plt.subplots(figsize=(20,4))
    cur_num = 0
    
    for f in files:
        ax.plot(f.get_data(), c=COLORS[cur_num], label=f.header)
        cur_num += 1
    
    plt.legend(loc='best');
    plt.show()

def save_files(files):
    # Error handling
    if not isinstance(files, list):
        raise TypeError("Sorry. 'files' must be list.")
    if not all(isinstance(f, FileIn) for f in files):
        raise TypeError("Sorry. items in 'files' must be FileIn type.")
    
    for f in files:
        f.export(loc="lib/data/test/")

if __name__ == "__main__":
    # Functional verification starts here
    print("--------Main file functional verification--------\n")
    
    allow_user_in = 0
    save_file_flag = 0
    align_original = 1
    if allow_user_in:
        user_in_ctrl()
    
    files_loc = "lib/data/"
    
    # FILECATEGORY = ['temp','google','music','omusic','youtube']
    use_temp = 0
    if use_temp:
        test_files = load_files(files_loc, FILECATEGORY[0], 2)
    else:
        test_files = load_files(files_loc, FILECATEGORY[1], 5, count_start=3)
    
    for f in test_files:
        print("File header is %s" %f.get_header())
        print("Overall average is %.2f" %f.get_average())
    
    reduced_files = get_reduced_files(test_files)
    
    reduced_fedges = adj.auto_align(reduced_files, tvalue="auto", neglect_pulse_width=2, skip_steps=12)
    
    plot_files(reduced_files)
    
    if align_original:
        adj.auto_align(test_files, tvalue="auto", neglect_pulse_width=2, skip_steps=12, input_edges=reduced_fedges)
        plot_files(test_files)
    
    if save_file_flag: save_files(reduced_files)
    
    print("--------Verification ends--------\n")