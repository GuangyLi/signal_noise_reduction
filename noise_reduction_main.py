import numpy as np
from lib.file_load import FileIn
from lib.func_avg import average_signal

if __name__ == "__main__":
    # Functional verification starts here
    print("--------Main file functional verification--------\n")
    test = FileIn("lib/data/google1.txt", 334)
    print("File located in %s" %test.get_location())
    print("File header is %s" %test.get_header())
    print(test.get_data())
    print("Overall average is %.2f" %test.get_average())
    print("The signal frequency is %d\n" %test.get_frequency())
    
    test_avg = average_signal(test.data, test.freq, 167)
    print(test_avg.data)
    print(test_avg.input_freq)
    print(test_avg.noise_freq)
    print("--------Verification ends--------\n")