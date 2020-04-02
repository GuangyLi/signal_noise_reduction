# Python program to load signal stored in a file with heading and value in each line
# Stored in a class with value of the data and sampling frequency

import sys
import numpy as np

class FileIn:
    # Initialize the class
    def __init__(self, input_file, input_freq, noise_freq):
        self.file_name = input_file
        self.input_freq = input_freq
        self.noise_freq = noise_freq
        self.data, self.header, self.average = self.file_load()
        self.fileloc = self.file_loc()
        
        # Internal flag to determine whether it's adjusted/aligned or not
        self.aligned = False
        self.adjusted = False
    
    # Embedded file loading function
    def file_load(self):
        contents = []
        head = self.file_name.split("/")[-1].split(".")[0]
        total, avg, data_num = 0, 0, 0
        
        try:
            file = open(self.file_name, 'r')
            for line in file:
                # Ignore any data which has type as message instead of value
                try:
                    value = float(line.strip('\n'))
                    # Ignore corrupted data which is too low or too high in value
                    if (value >= avg/10) and (value <= avg*10 or total == 0):
                        total += value
                        data_num += 1
                        avg = total/data_num
                        
                        contents.append(value)
                        
                except:
                    # Update header if internal message contains more detailed information
                    msg = line.strip('\n')
                    if head in msg:
                        head = msg
            
            file.close()
            
        except:
            err_msg = "ERROR: File " + self.file_name + " does not exist.\n"
            print(err_msg, file=sys.stderr, end='')
        
        data = np.array(contents, dtype=np.float32)
        return data, head, avg
    
    # Function that find the location fodler of the file
    def file_loc(self):
        loc = ""
        if "/" in self.file_name:
            for i in self.file_name.split("/")[:-1]:
                loc = loc+ i +"/"
        else:
            loc = "./"
        
        return loc
    
    def rename(self, new_name):
        self.file_name = new_name
    
    # Function that export the information in this class to a txt file
    def export(self, loc="auto", name="auto"):
        ############################
        ############TBD#############
        ############################
        return
        
    # Functions to return values
    def get_data(self):
        return self.data.copy()
    
    def get_max(self):
        return self.data.max()
    
    def get_min(self):
        return self.data.min()
    
    def get_data_size(self):
        return self.data.size
    
    def get_location(self):
        return self.fileloc
    
    def get_full_name(self):
        return self.file_name
    
    def get_header(self):
        return self.header
    
    def get_input_frequency(self):
        return self.input_freq
    
    def get_noise_frequency(self):
        return self.noise_freq
    
    def get_average(self):
        return self.average
        
if __name__ == "__main__":
    # Functional level verification starts here
    print("--------FileIn class functional verification--------\n")
    test = FileIn("data/google1.txt", 334, 167)
    print("File located in %s" %test.fileloc)
    print("File header is %s" %test.header)
    print(test.data)
    print("Overall average is %.2f" %test.average)
    print("The signal frequency is %d" %test.input_freq)
    print("The noise frequency is %d\n" %test.noise_freq)
    print("--------Verification ends--------\n")
