import numpy as np
from lib.file_load import FileIn

if __name__ == "__main__":
    # Functional verification starts here
    print("--------Main file functional verification--------\n")
    test = FileIn("lib/data/google1.txt", 334)
    print("File located in %s" %test.fileloc)
    print("File header is %s" %test.header)
    print(test.data)
    print("Overall average is %.2f" %test.average)
    print("The signal frequency is %d\n" %test.freq)
    print("--------Verification ends--------\n")