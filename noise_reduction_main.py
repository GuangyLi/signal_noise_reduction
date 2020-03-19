import time
import numpy as np
import matplotlib.pyplot as plt
#import noisereduce as nr
from lib.file_load import FileIn
from lib.func_avg import average_signal
from lib.func_pulse import remove_pulse
import lib.data_adjust as adj

if __name__ == "__main__":
    # Functional verification starts here
    print("--------Main file functional verification--------\n")
    
    # Flag determine whether use auto method or not and which method to use
    auto_avg = 0
    plot_smooth = 1
    plot_slope = 1
    avg_steps = 8
    allow_user_in = 0
    
    if allow_user_in:
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
    
    use_google = 1
    if use_google:
        test1 = FileIn("lib/data/google3.txt", 334, 167)
        test2 = FileIn("lib/data/google4.txt", 334, 167)
    else:
        test1 = FileIn("lib/data/temp1.txt", 334, 167)
        test2 = FileIn("lib/data/temp2.txt", 334, 167)    
    print("File located in %s" %test1.get_location())
    print("File header is %s" %test1.get_header())
    print(test1.get_data())
    print("Overall average is %.2f" %test1.get_average())
    print("The signal frequency is %d\n" %test1.get_input_frequency())
    
    temp_data = test1.get_data()
    
    test_avg1 = average_signal(test1)
    test_avg2 = average_signal(test2)
    print(test_avg1.data)
    print(test_avg1.input_freq)
    print(test_avg1.noise_freq)
    
    if auto_avg:
        if plot_slope:
            reduced_file1 = test_avg1.slope_average_data(steps="auto")
            reduced_file2 = test_avg2.slope_average_data(steps="auto")
        elif plot_smooth:
            reduced_file1 = test_avg1.generate_average_data(steps="auto", atype="smooth")
            reduced_file2 = test_avg2.generate_average_data(steps="auto", atype="smooth")
        else:
            reduced_file1 = test_avg1.generate_average_data(steps="auto", atype="step")
            reduced_file2 = test_avg2.generate_average_data(steps="auto", atype="step")
        
    else:
        if plot_slope:
            reduced_file1 = test_avg1.slope_average_data(steps=avg_steps)
            reduced_file2 = test_avg2.slope_average_data(steps=avg_steps)
        elif plot_smooth:
            reduced_file1 = test_avg1.generate_average_data(steps=avg_steps, atype="smooth")
            reduced_file2 = test_avg2.generate_average_data(steps=avg_steps, atype="smooth")
        else:
            reduced_file1 = test_avg1.generate_average_data(steps=avg_steps, atype="step")
            reduced_file2 = test_avg2.generate_average_data(steps=avg_steps, atype="step")
    
    reduced_files = [reduced_file1, reduced_file2]
    adj.auto_align(reduced_files, tvalue=600, neglect_pulse_width=2, skip_steps=12)
    #noisy_part = np.array(list(temp_data[860:])*5)
    #reduced_result = nr.reduce_noise(audio_clip=temp_data, noise_clip=noisy_part, verbose=False)
    
    fig, ax = plt.subplots(figsize=(20,4))
    ax.plot(temp_data, c='r', label='initial')
    
    # Whether plot smooth curve or not, or slope average result
    ax.plot(reduced_file1.data, c='b', label='reduced1')
    ax.plot(reduced_file2.data, c='g', label='reduced2')
    
    #ax.plot(noisy_part, c='g', label='noise')
    plt.legend(loc='best');
    plt.show()
    
    print("reduced data file name is %s" %reduced_file1.get_full_name())
    print("--------Verification ends--------\n")