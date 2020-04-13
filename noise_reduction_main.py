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
FILECATEGORY = ['temp','google','youtube','cnn','wiki','music','omusic']

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

def load_files(file_loc, file_cate, file_count, count_start = 1, wired = False, percentage = 100):
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
    if not isinstance(wired, bool):
        raise TypeError("Sorry. 'wired' must be boolean.")
    if not isinstance(percentage, int):
        raise TypeError("Sorry. 'percentage' must be int.")    
    
    if not os.path.exists(file_loc):
        print("Warning: Destion doesn't exist, %s created" %file_loc)
        os.mkdir(file_loc)
    
    # Check the sub directory that store the files
    ext_dirs = [f for f in os.listdir(file_loc) if ospath.isdir(ospath.join(file_loc, f))]
    percent_str = str(percentage)
    if wired:
        wiring = "Wired"
    elif file_cate == "temp":
        wiring = "temp"
        percent_str = "temp"
    else:
        wiring = "Wireless"
    
    ext_num = 0
    cur_dirs = []
    for ext_dir in ext_dirs:
        if (file_cate in ext_dir) and (wiring in ext_dir) and (percent_str in ext_dir):
            ext_num += 1
            cur_dirs.append(ext_dir)
    
    if ext_num == 0:
        raise TypeError("Sorry. %s related files doesn't exist in %s." %(file_cate, file_loc))
    
    dir_num = 0
    if ext_num > 1:
        print("Multiple directories detected, which one do you want to pick:")
        for i in range(ext_num):
            print("%d: %s" %(i, cur_dirs[i]))
        
        prompt_text = "Please type in the number of your directory: "
        while(1):
            user_in = input(prompt_text)
            try:
                dir_num = int(user_in)
            except:
                print("PLEASE ENTER INITGER ONLY!")
    
    # Check files in the sub directory
    file_loc = ospath.join(file_loc, cur_dirs[dir_num]) + "/"
    ext_files = [f for f in os.listdir(file_loc) if ospath.isfile(ospath.join(file_loc, f))]
    file_num = len(ext_files)
    
    if file_num > file_count:
        file_num = file_count
        ext_files = []
        for i in range(file_count):
            tmp_name = "trial" + str(i+count_start) + ".txt"
            ext_files.append(tmp_name)
    
    files = []
    for f in ext_files:
        filename_full = file_loc + f
        files.append(FileIn(filename_full, 334, 167, file_cate))
    
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
        tmp_lable = f.file_category + "_" + f.header 
        ax.plot(f.get_data(), c=COLORS[cur_num], label=tmp_lable)
        cur_num += 1
    
    plt.legend(loc='best');
    plt.show()

def save_files(files, file_category, separate_dir=False):
    # Error handling
    if not isinstance(files, list):
        raise TypeError("Sorry. 'files' must be list.")
    if not all(isinstance(f, FileIn) for f in files):
        raise TypeError("Sorry. items in 'files' must be FileIn type.")
    if not isinstance(file_category, str):
        raise TypeError("Sorry. 'file_category' must be string.")
    if not isinstance(separate_dir, bool):
        raise TypeError("Sorry. 'separate_dir' must be boolean.")        
    
    if separate_dir:
        for f in files:
            f.export(file_category, loc="lib/data/filtered/")
    else:
        for f in files:
            f.export(file_category)

if __name__ == "__main__":
    # Functional verification starts here
    print("--------Main file functional verification--------\n")
    
    allow_user_in = 0
    save_file_flag = 1
    align_original = 1
    if allow_user_in:
        user_in_ctrl()
    
    # FILECATEGORY = ['temp','google','youtube','cnn','wiki','music','omusic']
    
    pre_loc = "lib/data/"
    use_data = 3
    
    if use_data:
        test_files = load_files(pre_loc, FILECATEGORY[use_data], 5, count_start=1)
    else:
        test_files = load_files(pre_loc, FILECATEGORY[use_data], 2)
    
    for f in test_files:
        print("File header is %s" %f.get_header())
        print("Overall average is %.2f" %f.get_average())
    
    reduced_files = get_reduced_files(test_files)
    
    if use_data == 3:
        steps = 20
    elif use_data == 0:
        steps = 1
    else:
        steps = 12
    
    reduced_fedges = adj.auto_align(reduced_files, tvalue="auto", neglect_pulse_width=2, skip_steps=steps)
    
    plot_files(reduced_files)
    
    if align_original:
        adj.auto_align(test_files, tvalue="auto", neglect_pulse_width=2, skip_steps=steps, input_edges=reduced_fedges)
        plot_files(test_files)
    
    if save_file_flag: save_files(reduced_files, FILECATEGORY[use_data], separate_dir=True)
    
    print("--------Verification ends--------\n")