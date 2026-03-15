import encryption
import csv 
import re
import string

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

def newUser(username,password):
    personalkey = encryption.getKey()
    password = encryption.encrypt(password,personalkey)
    with open("loggin.txt", "a") as f:
         f.write(f"{username},{password},{personalkey}\n")



def logUser(username, password):
    try:
        with open("loggin.txt", "r") as f:
            reader = csv.reader(f)

            for row in reader:
                stored_username,stored_password,*key = row
                if stored_username == username:
                    decrypted_password = encryption.decrypt(stored_password, key)
                    if decrypted_password == password:
                        print("logged in")
                        return True
                    else:
                        print("incorrect password")
                        return False
            print("username doesn't match")
            return False
    except FileNotFoundError:
        print("Error: loggin.txt not found.")
        return False    

def passwordCheck(password):
    special_chars = re.escape(string.punctuation)
    pattern = rf"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[{special_chars}]).{{8,}}$"
    if re.match(pattern,password):
        return True
    else:
        return False

def userkey(search_username):
    with open("loggin.txt", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            username, password, key = row
            if username == search_username:
                return key

display = ("1.login\n2.signin\n3.exit")
def main():
    while True : 
        print(display)
        user_choice = input(":")
        if user_choice == "1" :
            username = input("what is your username? :")
            password = input("what is your password? :")
            logUser(username,password)
            if logUser(username,password) == True :
                pass
            else:
                pass     
        elif user_choice == "2":
            username = input("what is your username? :")
            password = input("what is your password? :")
            passwordCheck(password)
            newUser(username,password)
        elif user_choice == "3":
            break
