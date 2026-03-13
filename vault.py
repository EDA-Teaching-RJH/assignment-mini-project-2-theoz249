import Encryption
import csv 


try:
    with open("login.txt", "r") as f:
        print("File exists and is readable.")
except FileNotFoundError:
    print("File does not exist.")
    with open("login.txt", "w") as f:  
        f.write("username,password,key\n")   
    print("File is now confirmed to exist (or was just created).")
except IOError:
    print("Could not access or create the file.")
    pass

username = ""
password = ""
personalkey = ""
