# Python program to load signal stored in a file with heading and value in each line
# Stored in a class with value of the data and sampling frequency

import os
import os.path as ospath
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
    
    # Function that find the location folder of the file
    def file_loc(self):
        loc = ""
        if "/" in self.file_name:
            for i in self.file_name.split("/")[:-1]:
                loc = loc + i +"/"
        else:
            loc = "./"
        
        return loc
    
    def rename(self, new_name):
        self.file_name = new_name
        self.header = new_name.split("/")[-1]
    
    # Function that export the information in this class to a txt file
    def export(self, loc="auto", name="auto"):
        # Error handling
        if not isinstance(loc, str):
            raise TypeError("Sorry. 'files' must be string.")
        if not isinstance(name, str):
            raise TypeError("Sorry. 'files' must be str.")
        
        # Export location and file name generation
        ept_loc = ""
        ept_name = ""
        if loc == "auto":
            ept_loc = self.fileloc
        else:
            if not os.path.exists(loc):
                print("Warning: Destion doesn't exist, %s created" %loc)
                os.mkdir(loc)
            ept_loc = loc
        
        if name == "auto":
            ept_name = self.header
            if (".txt" in ept_name) and (ept_name[-4:] == ".txt"):
                ept_name = ept_name[:-4]
            
            if self.aligned:
                ept_name += "_aligned"
            elif self.adjusted:
                ept_name += "_adjusted"
                
            ept_name += ".txt"
            
        else:
            if not (".txt" in name):
                print("Warning: file type doesn't recognized, txt file created")
                name += ".txt"
            ept_name = name
        
        # Not overwrite exist files
        ext_filenames = [f for f in os.listdir(ept_loc) if ospath.isfile(ospath.join(ept_loc, f))]
        ext_num = -1
        for ext_name in ext_filenames:
            if ept_name[:-4] in ext_name:
                try:
                    i = int(ext_name[-5])
                except:
                    i = 0
                    
                i += 1
                if i > ext_num:
                    ext_num = i
        
        if ext_num is not -1:
            ept_name = ept_name[:-4] + ("_%d.txt" %ext_num)
        
        # Create file and store data in
        ept_file = open(ospath.join(ept_loc, ept_name), "w+")
        for d in self.data:
            ept_file.write("%d\r" %d)
        
        ept_file.close()
        
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
    test = FileIn("data/temp1.txt", 334, 167)
    print("File located in %s" %test.fileloc)
    print("File header is %s" %test.header)
    print(test.data)
    print("Overall average is %.2f" %test.average)
    print("The signal frequency is %d" %test.input_freq)
    print("The noise frequency is %d\n" %test.noise_freq)
    test.aligned = 1
    test.export()
    print("--------Verification ends--------\n")
