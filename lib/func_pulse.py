# Python function to remove the pulse comes from noise instead of normal signal
# The decision of what kind of pulse comes from calculation based on frequency

import sys
import numpy as np
from lib.file_load import FileIn
#from file_load import FileIn

############################
############TBD#############
############################

class remove_pulse():
    # Initialize the class
    def __init__(self, input_file):
        # Error handling
        if not isinstance(input_file, FileIn):
            raise TypeError("Sorry. 'input_file' must be FileIn type.")
        
        self.file = input_file
        self.data = input_file.data
        self.input_freq = input_file.input_freq
        self.noise_freq = input_file.noise_freq
        
    # Return the result in FileIn type
    def return_file(self, result_data, steps="auto"):
        input_name = self.file.file_name
        temp_file = FileIn(input_name, self.input_freq, self.noise_freq)
        
        temp_file.data = result_data
        temp_file.rename(input_name[:-4] + "_reduced_pulse_" + str(steps) + ".txt")
        
        return temp_file

if __name__ == "__main__":
    # Functional level verification starts here
    print("--------File out functional verification--------\n")
    test = FileIn("data/google1.txt", 334, 167)
    rp = remove_pulse(test)
    print("--------Verification ends--------\n")