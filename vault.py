import encryption
import csv 
import re

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

def newUser():
    personalkey = encryption.getKey()
    username = input(":")
    password = input(":")
    password = encryption.encrypt(password,personalkey)
    with open("login.txt", "a") as f:
         f.write(f"{username},{password},{personalkey}\n")



def logUser():
    logIn = False
    username = input(":")
    password = input(":")
    with open("loggin.txt", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            stored_username,stored_password,key = row
            if stored_username == username:
                decrypted_password = encryption.decrypt(stored_password,key)
                if decrypted_password == password:
                    print("logged in")
                    logIn = True 
                    return logIn
                else:
                    print("incorrect password")
                    return logIn
            else:
                print("username doesn't match")
                return logIn