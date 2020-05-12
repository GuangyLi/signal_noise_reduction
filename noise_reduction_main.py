import time
import os
import os.path as ospath
import numpy as np
import matplotlib.pyplot as plt
import random

#import noisereduce as nr
from lib.file_load import FileIn
from lib.func_avg import average_signal
from lib.func_pulse import remove_pulse
import lib.data_adjust as adj
from lib.cnn import VGG_result

# Library for signal feature generation function
from scipy.fftpack import fft
from scipy.signal import welch

# Library for machine learning
from sklearn.utils import shuffle
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier, BaggingClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

# Nerual Network related
import keras
from keras import layers
from keras.layers import Input,Reshape,ZeroPadding2D,Conv2D,Dropout,Flatten,Dense,Activation,MaxPooling2D,AlphaDropout,BatchNormalization
import keras.models as Model
from keras.regularizers import *
from keras.optimizers import adam
from keras.applications.vgg16 import VGG16
import tensorflow as tf


# Global variable that contains all allowed color in matplotlib, use html hex string for greater range
COLORS = ['b','g','r','c','m','y','k','w']
FILECATEGORY = ['temp','google','youtube','cnn','wiki','music','omusic']

# Function that allow user input to specifically define what parameter used to process the data
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

# Function to load all files in that location with input category and counting number
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
        #if (file_cate in ext_dir) and (wiring in ext_dir) and (percent_str in ext_dir):
        if (file_cate in ext_dir):
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
    expect_files = [f for f in os.listdir(file_loc) if ospath.isfile(ospath.join(file_loc, f))]
    file_num = len(expect_files)
    
    ext_files = []
    if file_num > file_count:
        file_num = file_count
        for i in range(file_count):
            tmp_name = "t" + str(i+count_start) + ".txt"
            ext_files.append(tmp_name)
    else:
        ext_files = expect_files
    
    
    files = []
    for f in ext_files:
        filename_full = file_loc + f
        files.append(FileIn(filename_full, 334, 167, file_cate))
    
    return files

# Function that return a list of filtered version of items in files list
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
                tmp_reduced.append(tmp_test.generate_average_data(steps="auto", atype="smooth"))
            else:
                tmp_reduced.append(tmp_test.generate_average_data(steps="auto", atype="step"))
        else:
            if plot_slope:
                tmp_reduced.append(tmp_test.slope_average_data(steps=avg_steps))
            elif plot_smooth:
                tmp_reduced.append(tmp_test.generate_average_data(steps=avg_steps, atype="smooth"))
            else:
                tmp_reduced.append(tmp_test.generate_average_data(steps=avg_steps, atype="step"))
    
    return tmp_reduced

# Function to plot data in files list
def plot_data(files, mode="File"):
    # Error handling
    if not isinstance(files, list):
        raise TypeError("Sorry. 'files' must be list.")
    if not isinstance(mode, str):
        raise TypeError("Sorry. 'mode' must be string.")
    if mode == "File":
        if not all(isinstance(f, FileIn) for f in files):
            raise TypeError("Sorry. items in 'files' must be FileIn type in File mode.")
    elif mode == "data":
        if not all(isinstance(f, list) for f in files):
            raise TypeError("Sorry. items in 'files' must be list type in Data mode.")        
    
    if len(files) > len(COLORS):
        print("Warning: too many files might cause unrecognized output!")
    
    fig, ax = plt.subplots(figsize=(20,4))
    files_size = len(files)
    color_step = int(0xffffff/(files_size))
    cur_num = 0
    
    if (mode == "File"):
        if (files_size <= 8):
            for f in files:
                tmp_lable = f.file_category + "_" + f.header 
                ax.plot(f.get_data(), c=COLORS[cur_num], label=tmp_lable)
                cur_num += 1
        else:
            for f in files:
                tmp_lable = f.file_category + "_" + f.header 
                hex_str = hex(color_step*(cur_num+1)-1)[2:]
                color_str = "#" + "0"*(6-len(hex_str)) + hex_str
                ax.plot(f.get_data(), c=color_str, label=tmp_lable)
                cur_num += 1
    elif (mode == "Data"):
        for f in files:
            tmp_lable = ("data %d" %cur_num)
            hex_str = hex(color_step*(cur_num+1)-1)[2:]
            color_str = "#" + "0"*(6-len(hex_str)) + hex_str
            ax.plot(f, c=color_str, label=tmp_lable)
            cur_num += 1        
    
    plt.legend(loc='best');
    plt.show()

# Function to export files in the files list
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

def get_fft_values(y_values, T, N, f_s):
    f_values = np.linspace(0.0, 1.0/(2.0*T), N//2)
    fft_values_ = fft(y_values)
    fft_values = 2.0/N * np.abs(fft_values_[0:N//2])
    return f_values, fft_values

def get_psd_values(y_values, f_s):
    f_values, psd_values = welch(y_values, fs=f_s)
    return f_values, psd_values

def get_fft_files_10(files, N, f_values=334):
    fft_files = []
    for f in files:
        fft_files.append(get_fft_values(f.data, 1/334, N, 334)[1][:10])
    
    return f_values, fft_files

def get_psd_files_10(files, f_values=334):
    psd_files = []
    for f in files:
        psd_files.append(get_psd_values(f.data, 334)[1][:10])
    
    return f_values, psd_files

# Label transfer function
def label_reshape(y_label, lb, act="forward"):
    # Change the format of label from (?,1) to (?,10) as 3 = [0,0,1,...,0,0,0]
    if (act == "forward"):
        y_label_reshaped = lb.transform(y_label)
    # Change the format
    elif (act == "backward"):
        y_label_reshaped = lb.inverse_transform(y_label)
    return y_label_reshaped

# Use CPU, some problem on cuDNN
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

if __name__ == "__main__":
    # Functional verification starts here
    print("--------Main file functional verification--------\n")
    
    # How many files expected, if 0, based on prediction function
    file_num = 0
    
    # Allow user input to control flag or not
    allow_user_in = 0
    
    # Output data in txt file or not
    save_file_flag = 0
    
    # Automatically determine avg_steps or not
    auto_avg = 0
    avg_steps = 8
    
    # if plot_slope, use slope_avg; elif plot_smooth, use smooth_avg; else, use step_avg
    plot_slope = 1
    plot_smooth = 1    
    
    # Align file and raw data or not
    align_files = 1
    align_original = 1 # also determine use raw in machine learning or not
    print_unaligned = 0
    
    # Load multiple files and apply machine laerning
    load_multiple = 1
    
    # 1 to use cnn, 0 to use adaboost
    use_cnn = 1
    
    # Generate save model name
    model_name = ""
    if plot_slope:
        model_name += "_slope"
    elif plot_smooth:
        model_name += "_smooth"
    else:
        model_name += "_step"
    
    if align_files:
        model_name += "_aligned"
    else:
        model_name += "_unaligned"
        
    if align_original:
        model_name += "_raw"
    else:
        model_name += "_filtered"    
    
    if load_multiple:
        
        # FILECATEGORY = ['temp','google','youtube','cnn','wiki','music','omusic']
        
        pre_loc = "lib/data/Testing Data/"        
        use_files = [1,2,3]
        steps = [9,10,6]
        files_size = 50
        files_cate_num = len(use_files)
        
        all_files = []
        all_labels = []
        
        # Load all files and labels
        for i in range(files_cate_num):
            
            test_files = load_files(pre_loc, FILECATEGORY[use_files[i]], files_size, count_start=1)
            reduced_files = get_reduced_files(test_files)
            
            if align_files:
                reduced_fedges, invalid_edges = adj.auto_align(reduced_files, tvalue="auto", neglect_pulse_width=2, skip_steps=steps[i])
            
                if align_original:
                    adj.auto_align(test_files, tvalue="auto", neglect_pulse_width=2, skip_steps=steps[i], input_edges=reduced_fedges)            
            
                # Print unrecognized plots for debugging
                num_negative = len(invalid_edges)
                print("There were %d unrecognized edges in file category %d." %(num_negative,i))
            
            if align_original:
                all_files.extend(test_files)
            else:
                all_files.extend(reduced_files)
                
            #plot_data(all_files[:(i+1)*50])
            
            all_labels.extend([FILECATEGORY[use_files[i]]]*files_size)
            
        adj.auto_adjust(all_files)
        
        #=================================================================
        #=======================Machine Learning=========================
        #=================================================================
        
        # Here starts the feature generation part
        data_length = len(all_files[0].data)
        print(data_length)
        
        f_values, files_fft_values = get_fft_files_10(all_files, data_length)
        f_values, files_psd_values = get_psd_files_10(all_files)
        
        all_features = []
        for i in range(files_size*files_cate_num):
            all_features.append([])
            
            # Merge fft, psd and data together
            all_features[i].extend(files_fft_values[i])
            all_features[i].extend(files_psd_values[i])
            all_features[i].extend(all_files[i].data[:1004])
            
            
        all_features = np.array(all_features)
        all_labels = np.array(all_labels)
        data_length = 1024
        
        # Randomly split the training and testing set
        X_train, X_test, y_train, y_test = train_test_split(all_features, all_labels, test_size=0.9, random_state=random.randint(1,255))
        
        print(X_train.shape)
        
        if use_cnn:
            # Binary encoder
            lb = preprocessing.LabelBinarizer()
            lb.fit(y_train)
            
            y_train_reshaped = label_reshape(y_train, lb, act="forward")
            y_test_reshaped = label_reshape(y_test, lb, act="forward")            
            
            p_train_loss, p_test_loss, p_train_acc, p_test_acc = VGG_result(X_train, X_test, y_train_reshaped, y_test_reshaped, 
                                                                            data_length, files_cate_num, train=False, model_name=model_name)
            
            # Calculate accuracy of result from loss model
            p_train_loss_recovered = label_reshape(p_train_loss, lb, act="backward")
            p_test_loss_recovered = label_reshape(p_test_loss, lb, act="backward")

            Acu_Train_loss = accuracy_score(y_train, p_train_loss_recovered)
            Acu_Test_loss = accuracy_score(y_test, p_test_loss_recovered)
            
            # Calculate accuracy of result from accuracy model
            p_train_acc_recovered = label_reshape(p_train_acc, lb, act="backward")
            p_test_acc_recovered = label_reshape(p_test_acc, lb, act="backward")

            Acu_Train_acc = accuracy_score(y_train, p_train_acc_recovered)
            Acu_Test_acc = accuracy_score(y_test, p_test_acc_recovered)
            
            print("\nItr #%d Acu_Train_loss is %.4f" %(i, Acu_Train_loss))
            print("Itr #%d Acu_Test_loss is %.4f\n" %(i, Acu_Test_loss))
            print("\nItr #%d Acu_Train_acc is %.4f" %(i, Acu_Train_acc))
            print("Itr #%d Acu_Test_acc is %.4f\n" %(i, Acu_Test_acc))
        else:
            tree = DecisionTreeClassifier(criterion='entropy', max_depth= 20)
            clf = AdaBoostClassifier(base_estimator=tree, n_estimators=1024).fit(X_train, y_train)
            
            p_train = clf.predict(X_train)
            p_test = clf.predict(X_test)
            
            Acu_Train = accuracy_score(y_train, p_train)
            Acu_Test = accuracy_score(y_test, p_test)
            Err_Train = 1-Acu_Train
            Err_Test = 1-Acu_Test
            
            print("\n\nTraining set prediction accuracy is %.2f%%." %(Acu_Train*100))
            print("Testing set prediction accuracy is %.2f%%." %(Acu_Test*100))
        
    else:
        # User input that can change the control variable
        if allow_user_in:
            user_in_ctrl()
        
        # FILECATEGORY = ['temp','google','youtube','cnn','wiki','music','omusic']
        pre_loc = "lib/data/Testing Data/"
        use_data = 2
        
        if use_data == 1:
            files_size = 50
        elif use_data == 0:
            files_size = 2
        elif use_data == 2:
            files_size = 50
        elif use_data == 3:
            files_size = 50
        else:
            files_size = 5
        
        # Load files into a list
        if use_data:
            test_files = load_files(pre_loc, FILECATEGORY[use_data], files_size, count_start=1)
        else:
            test_files = load_files(pre_loc, FILECATEGORY[use_data], files_size)
        
        for f in test_files:
            print( "File header is %s, and Overall average is %.2f" %(f.get_header(), f.get_average()) )
        
        # Filter the data in files
        reduced_files = get_reduced_files(test_files)
        reduced_files_noalign = list(reduced_files)
        
        if use_data == 0:
            steps = 1
        elif use_data == 1:
            steps = 9
        elif use_data == 3:
            steps = 6
        else:
            steps = 10
            
        # Plot unaligned raw and filtered data
        if print_unaligned:
            print("\nHere are unaligned raw data:")
            plot_data(test_files)
            print("\nHere are unaligned filtered data:")
            plot_data(reduced_files)
        
        # Align and adjust the data in files
        reduced_fedges, invalid_edges = adj.auto_align(reduced_files, tvalue="auto", neglect_pulse_width=2, skip_steps=steps)
        
        # Print unrecognized plots for debugging
        num_negative = len(invalid_edges)
        print("There were %d unrecognized edges." %num_negative)
        
        if (num_negative and num_negative <= 8):
            fig, ax = plt.subplots(figsize=(20,4))
            j = 0
            for i in invalid_edges:
                ax.plot(reduced_files_noalign[i].get_data(), c=COLORS[j], label=reduced_files_noalign[i].header)
                j += 1
                    
            plt.legend(loc='best');
            plt.show()
        
        # Plot all aligned and filtered data
        print("\nHere are aligned filtered data:")
        plot_data(reduced_files)
        
        # Align the raw data and plot them
        if align_original:
            adj.auto_align(test_files, tvalue="auto", neglect_pulse_width=2, skip_steps=steps, input_edges=reduced_fedges)
            print("\nHere are aligned raw data:")
            plot_data(test_files)
        
        # Export filtered files
        if save_file_flag: save_files(reduced_files, FILECATEGORY[use_data], separate_dir=True)
    
    
    print("\n--------Verification ends--------")