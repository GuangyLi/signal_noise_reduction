# Python program that takes numpy array as input signal
# and reduce the effect of noise using average function

import statistics
import numpy as np
import random
from lib.file_load import FileIn
#from file_load import FileIn

class average_signal:
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
    def return_file(self, result_data, steps="auto", atype="step"):
        input_name = self.file.file_name
        temp_file = FileIn(input_name, self.input_freq, self.noise_freq)
        
        temp_file.data = result_data
        temp_file.rename(input_name[:-4] + "_reduced_avg_" + atype + "_" + str(steps) + ".txt")
        
        return temp_file
        
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
            
            return self.return_file(temp_data, steps=steps, atype=atype)
        
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
            
            for s in range(steps*2):
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
        return self.return_file(temp_result, steps=steps, atype=atype)
    
    # Function generates step to average automatically based on frequencies
    def auto_gen_step(self):
        # Input frequency stands for # signal observed per second
        # Noise frequency stands for # pulse of noise per second
        cal_step = int(self.input_freq/self.noise_freq)*2
        return cal_step
    
    # Function that returns the average of each slope in certain step
    def slope_average_data(self, steps="auto"):
        # Error handling
        if steps != "auto":
            if not isinstance(steps, int):
                raise TypeError("Sorry. 'steps' must be an integer.")
            if not steps >= 0:
                raise ValueError("Sorry. 'steps' must be zero or positive.")
        else:
            steps = self.auto_gen_step()
        
        temp_data = np.copy(self.data)
        avg_cur_slope = np.array([])
        len_steps = int(len(temp_data)/steps)
        
        for i in range(len_steps):
            
            first = i*steps
            last = (i+1)*steps
            if last >= len(temp_data):
                cur_avg = (temp_data[first] + temp_data[first-steps])/2
            else:
                cur_avg = (temp_data[last] + temp_data[first])/2
            
            avg_cur_slope = np.append(avg_cur_slope, cur_avg)
        
        i = 1
        middle = int(steps/2)
        while i < (len_steps-1):
            avg_bfr_step = (avg_cur_slope[i] - avg_cur_slope[i-1])/steps
            avg_aft_step = (avg_cur_slope[i+1] - avg_cur_slope[i])/steps
            for s in range(steps):
                cur_pos = i*steps + s
                
                if s <= middle:
                    temp_data[cur_pos] = avg_cur_slope[i] - avg_bfr_step*(middle-s)
                else:
                    temp_data[cur_pos] = avg_cur_slope[i] + avg_aft_step*(s-middle)
            i += 1
        
        avg_ini_step = (avg_cur_slope[1] - avg_cur_slope[0])/steps
        avg_fin_step = (avg_cur_slope[-1] - avg_cur_slope[-2])/steps
        
        for s in range(steps*2):
            ini_pos = s
            fin_pos = -(s+1)
            
            if s <= middle:
                temp_data[ini_pos] = avg_cur_slope[0] - avg_ini_step*(middle-s)
                temp_data[fin_pos] = avg_cur_slope[-1] + avg_fin_step*(middle-s)
            else:
                temp_data[ini_pos] = avg_cur_slope[0] + avg_ini_step*(s-middle)
                temp_data[fin_pos] = avg_cur_slope[-1] - avg_fin_step*(s-middle)
        
        return self.return_file(temp_data, steps=steps, atype="slope")

if __name__ == "__main__":
    # Functional level verification starts here
    '''
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
    test_result = test.slope_average_data(steps=2)
    print("test input is:")
    print(test_in)
    print("test result is:")
    print(test_result)        
    print("--------Verification ends--------\n")
    '''