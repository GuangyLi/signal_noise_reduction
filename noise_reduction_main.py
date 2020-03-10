import time
import numpy as np
import matplotlib.pyplot as plt
import noisereduce as nr
from lib.file_load import FileIn
from lib.func_avg import average_signal
from lib.file_out import file_out
import lib.data_adjust as adj

if __name__ == "__main__":
    # Functional verification starts here
    print("--------Main file functional verification--------\n")
    test = FileIn("lib/data/google2.txt", 334)
    print("File located in %s" %test.get_location())
    print("File header is %s" %test.get_header())
    print(test.get_data())
    print("Overall average is %.2f" %test.get_average())
    print("The signal frequency is %d\n" %test.get_frequency())
    
    temp_data = test.data
    
    test_avg = average_signal(temp_data, test.freq, 167)
    print(test_avg.data)
    print(test_avg.input_freq)
    print(test_avg.noise_freq)
    
    # Whether use auto method or not
    auto_avg = 0
    plot_smooth = 1
    plot_slope = 1
    
    if auto_avg:
        if plot_slope:
            reduced_slope = test_avg.slope_average_data(steps="auto")
        elif plot_smooth:
            reduced_result_smooth = test_avg.generate_average_data(steps="auto", atype="smooth")
        else:
            reduced_result_step = test_avg.generate_average_data(steps="auto", atype="step")
        
    else:
        if plot_slope:
            reduced_slope = test_avg.slope_average_data(steps=8)
        elif plot_smooth:
            reduced_result_smooth = test_avg.generate_average_data(steps=16, atype="smooth")
        else:
            reduced_result_step = test_avg.generate_average_data(steps=16, atype="step")
    
    #noisy_part = np.array(list(temp_data[860:])*5)
    #reduced_result = nr.reduce_noise(audio_clip=temp_data, noise_clip=noisy_part, verbose=False)
    
    fig, ax = plt.subplots(figsize=(20,4))
    ax.plot(temp_data, c='b', label='initial')
    
    # Whether plot smooth curve or not, or slope average result
    if plot_slope:
        ax.plot(reduced_slope, c='r', label='reduced')
    elif plot_smooth:
        ax.plot(reduced_result_smooth, c='r', label='reduced')
    else:
        ax.plot(reduced_result_step, c='r', label='reduced')
    
    
    #ax.plot(noisy_part, c='g', label='noise')
    plt.legend(loc='best');
    plt.show()
    print("--------Verification ends--------\n")