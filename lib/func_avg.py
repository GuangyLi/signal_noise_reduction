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
        
    def generate_average_data(self, steps="auto", atype="step"):
        validtype = ["step", "smooth"]
        
        # Error handling
        if steps != "auto":
            if not isinstance(steps, int):
                raise TypeError("Sorry. 'steps' must be an integer.")
            if not steps >= 0:
                raise ValueError("Sorry. 'steps' must be zero or positive.")
        else:
            steps = self.auto_gen_step()
            
        if not atype in validtype:
            raise TypeError("Invalid average type detected")
        
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
            
            temp_data[cur_pos:] = avg_cur_step
            
            return temp_data
        
        # Function that calculate the average of # steps and generate a smooth transition
        def calculate_smooth_average(data_in, steps):
            temp_data = np.copy(data_in)
            avg_cur_steps = np.array([])
            len_steps = int(len(temp_data)/steps)
            
            for i in range(len_steps):
                
                last = (i+1)*steps
                if last >= len(temp_data):
                    cur_step = temp_data[i*steps:]
                else:
                    cur_step = temp_data[i*steps:last]
                
                avg_cur_step = np.mean(cur_step, dtype=np.float32)
                avg_cur_steps = np.append(avg_cur_steps, avg_cur_step)
            
            i = 1
            middle = int(steps/2)
            while i < (len_steps-1):
                avg_bfr_step = (avg_cur_steps[i] - avg_cur_steps[i-1])/steps
                avg_aft_step = (avg_cur_steps[i+1] - avg_cur_steps[i])/steps
                for s in range(steps):
                    cur_pos = i*steps + s
                    
                    if s <= middle:
                        temp_data[cur_pos] = avg_cur_steps[i] - avg_bfr_step*(middle-s)
                    else:
                        temp_data[cur_pos] = avg_cur_steps[i] + avg_aft_step*(s-middle)
                i += 1
            
            avg_ini_step = (avg_cur_steps[1] - avg_cur_steps[0])/steps
            avg_fin_step = (avg_cur_steps[-1] - avg_cur_steps[-2])/steps
            
            for s in range(steps):
                ini_pos = s
                fin_pos = -(s+1)
                
                if s <= middle:
                    temp_data[ini_pos] = avg_cur_steps[0] - avg_ini_step*(middle-s)
                    temp_data[fin_pos] = avg_cur_steps[-1] + avg_fin_step*(middle-s)
                else:
                    temp_data[ini_pos] = avg_cur_steps[0] + avg_ini_step*(s-middle)
                    temp_data[fin_pos] = avg_cur_steps[-1] - avg_fin_step*(s-middle)
            
            return temp_data
        
        if atype == "step":
            temp_result = calculate_step_average(self.data, steps)
        if atype == "smooth":
            temp_result = calculate_smooth_average(self.data, steps)
        return temp_result
    
    # Function generates step to average automatically based on frequencies
    def auto_gen_step(self):
        # Input frequency stands for # signal observed per second
        # Noise frequency stands for # pulse of noise per second
        cal_step = int(self.input_freq/self.noise_freq)*2
        return cal_step

if __name__ == "__main__":
    # Functional level verification starts here
    print("--------average_signal class functional verification--------\n")
    test_in = []
    for i in range(100):
        test_in.append(random.randint(0,200))
    test_in = np.array(test_in)
    test = average_signal(test_in, 334, 167)
    test_result = test.generate_average_data(steps="auto", atype="step")
    print("test input is:")
    print(test_in)
    print("test result is:")
    print(test_result)
    test_result = test.generate_average_data(steps="auto", atype="smooth")
    print("test input is:")
    print(test_in)
    print("test result is:")
    print(test_result)    
    print("--------Verification ends--------\n")