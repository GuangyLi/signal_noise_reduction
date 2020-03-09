# Python program to load signal stored in a file with heading and value in each line
# Stored in a class with value of the data and sampling frequency

import numpy as np

class FileIn:
    # Initialize the class
    def __init__(self, input_file, input_freq):
        self.data, self.header, self.average = self.file_load(input_file)
        self.freq = input_freq
        
        loc = ""
        if "/" in input_file:
            for i in input_file.split("/")[:-1]:
                loc = loc+ i +"/"
        else:
            loc = "./"
        self.fileloc = loc
    
    # Embedded file loading function
    def file_load(self, file_name):
        contents = []
        head = file_name.split("/")[-1].split(".")[0]
        total, avg, data_num = 0, 0, 0
        
        try:
            file = open(file_name, 'r')
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
            print("ERROR: File " + file_name + " does not exist.\n")
        
        data = np.array(contents, dtype=np.float32)
        return data, head, avg
        
if __name__ == "__main__":
    # Functional verification
    print("--------FileIn class functional verification--------\n")
    test = FileIn("data/google1.txt", 334)
    print("File located in %s" %test.fileloc)
    print("File header is %s" %test.header)
    print(test.data)
    print("Overall average is %.2f" %test.average)
    print("The signal frequency is %d\n" %test.freq)
    print("--------Verification ends--------\n")
