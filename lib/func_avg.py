# Python program that takes numpy array as input signal
# and reduce the effect of noise using average function

import statistics
import numpy as np
import random

class average_signal:
    # Initialize the class
    def __init__(self, input_data, input_freq, noise_freq):
        self.data = input_data
        self.input_freq = input_freq
        self.noise_freq = noise_freq
        
    def generate_average_data(self, steps):
        
        # Error handling
        if not isinstance(steps, int):
            raise TypeError("Sorry. 'steps' must be an integer.")
        if not steps >= 0:
            raise ValueError("Sorry. 'steps' must be zero or positive.")
        
        # Function that calculate the average of # steps
        def calculate_step_average(data_in, steps):
            temp_data = np.copy(data_in)
            for i in range(int(len(temp_data)/steps)):
                
                last = (i+1)*steps
                if last >= len(temp_data):
                    cur_step = temp_data[i*steps:]
                else:
                    cur_step = temp_data[i*steps:last]
                
                avg_cur_step = np.mean(cur_step, dtype=np.float32)
                
                for s in range(steps):
                    cur_pos = i*steps + s
                    if cur_pos < len(temp_data):
                        temp_data[cur_pos] = avg_cur_step
                
            return temp_data
        
        temp_result = calculate_step_average(self.data, steps)
        return temp_result

if __name__ == "__main__":
    # Functional level verification starts here
    print("--------average_signal class functional verification--------\n")
    test_in = []
    for i in range(100):
        test_in.append(random.randint(0,200))
    test_in = np.array(test_in)
    test = average_signal(test_in, 334, 167)
    test_result = test.generate_average_data(5)
    print("test input is:")
    print(test_in)
    print("test result is:")
    print(test_result)
    print("--------Verification ends--------\n")