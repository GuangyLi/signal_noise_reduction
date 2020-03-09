# Python program that takes numpy array as input signal
# and reduce the effect of noise using average function

import numpy as np

class average_signal:
    # Initialize the class
    def __init__(self, input_data, input_freq, noise_freq):
        self.data = input_data
        self.input_freq = input_freq
        self.noise_freq = noise_freq
        

if __name__ == "__main__":
    # Functional level verification starts here
    print("--------average_signal class functional verification--------\n")
    print("--------Verification ends--------\n")