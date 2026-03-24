import encryption #my own encryption modual
import json
import re
import string

#this makes sure that a file to write the login information of the user always exists when you run the program  
try:
    with open("loggin.json", "r") as f:#tries to open a file called "loggin.json" in read mode 
        print("File exists and is readable.")# if it opens it shows this messege 
except FileNotFoundError:
    with open("loggin.json", "w") as f:  #whenever there is a file not found error the code create the file instead of crashing 
        pass#the file that just got created has no contents in it
    print("file created")
except IOError:
    print("Could not access or create the file.")#if the file cannot be created or accessed for some reason then the code shows this to the user 
    pass

username = ""
password = ""
personalkey = ""

def newUser(username,password):#this function adds a new users login information into the login file 
    personalkey = encryption.getKey()#uses the getKey funtion from the encrytion modual to create a mostly unique personal key for the user 
    password = encryption.encrypt(password, personalkey)#uses the encrypt funtion from the encrytion modual to encrypt the users password using their personal key 
    user_data = {
        "username": username,
        "password": password,
        "key": personalkey
    }#a json format list that will contain the login information of every user such as their username , their encrypted password and their key 
    with open("loggin.json", "a", newline = '') as f:#opens the login file in apend mode
        f.write(json.dumps(user_data) + "\n")#dumps user data into login file
    print("Account created successfully!")



def logUser(username, password):#this function allows existing users to login
    try:
        with open("loggin.json", "r") as f:#tries to open the login file
            for line in f:#loops for every line in the login file
                user = json.loads(line)#converts every line in the json file into python format 
                if user["username"] == username:#checks if the username matches any of the username in the file
                    decrypted_password = encryption.decrypt(user["password"], user["key"])#decrypts every password in the file
                    if decrypted_password == password:#checks if the password matches any of the passwords in the file
                        print("logged in")
                        return True#if the username and password match then the login funtion returns true
                    else:
                        print("incorrect password")
                        return False#if they dont the funtion returns false
            print("username doesn't match")
            return False#if username doesnt match function returns false
    except FileNotFoundError:
        print("Error: loggin.txt not found.")
        return False# if the fie doesnt exist the fuction retuns fase

def passwordCheck(password):#checks if the password is strong enough
    special_chars = re.escape(string.punctuation) # creates a list of special characters that the regex fuction wont take in as a command 
    pattern = rf"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[{special_chars}]).{{8,}}$"# this list is the list of commands the regex funtion will use to check the passwords strength
    #?=.*[a-z] this command checks for atleast one repetition of a lower case letter
    #?=.*[A-Z] this does the same for uppercase letters
    #?=.*\d this checks for atleast one repetition of a digit
    #?=.*[{special_chars}] chechs for atlest one character in the special character list
    #{8,} makes sure the legth of the password is 8 characters long
    if re.match(pattern,password):
        return True#if the regex funtion matches then the fuction returs true
    else:
        return False#if the regex funtion doesnt match then the fuction returs false

def manage_vault(username, key):#this funtion is the vault system
    filename = f"vault_{username}.json"#stores the name of the persons vault in this variable
    try:
        with open(filename, "r") as f:#tryes to open the file in read mode
            encrypted_items = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):#if the file doesnt exist it creates it 
        with open(filename,"w") as f:
            pass
        encrypted_items = []
    while True:
        print(f"\n--- {username.uper()}'S VAULT ---")
        print(f"Total secrets: {len(encrypted_items)}")
        choice = input("1. Add secret\n2. View/Remove Secrets\n3. Logout\n: ")# asks the user for an option
        if choice == "1":
            secret = input("Enter secret to store: ") # if user chooses the first option the code asks the user to add an item 
            enc_secret = encryption.encrypt(secret, key)# uses the users key to encrypt the item
            encrypted_items.append(enc_secret)#adds that item to the ecrypted items list
            with open(filename, "w") as f:
                json.dump(encrypted_items, f)#adds all the contents of the ectypted items list into the json file in jsonformat
            print("Secret encrypted and added.")
        elif choice == "2":#if user chooses option 2 ...
            if not encrypted_items:#checks if vault contains any items 
                print("Vault is empty.")
                continue
            print("\n--- Your Secrets ---")#if vault does conatin items ...
            for i, enc_val in enumerate(encrypted_items):# the iems will be dispalyd and automaicaly counted by the enumerate fution 
                decrypted = encryption.decrypt(enc_val,key)
                print(f"{i+1}.{decrypted}")
            rem = input("\nRemove # (or 'b' to go back): ")#once the loop is finished the user is asked to remove an item by using the items index or return to the vault main menue 
            if rem.lower() == "b":
                continue
            elif rem.isdigit():#if the user inputs a digit the code will use that digit to find an index for an item and remove the item in that index
                idx = int(rem) - 1
                if 0 <= idx < len(encrypted_items):
                    encrypted_items.pop(idx)
                    with open(filename, "w") as f:
                        json.dump(encrypted_items, f)
                    print(f"Successfully removed item #{rem}")
                else:
                    print("Invalid number. No item removed.")
        elif choice == "3":# if user chooses option 3 it stops the funtion
            print("Vault saved and locked.")
            break


def userKey(search_username):#this fuuntion fetches a specific users key from the loggin file using the personsn username
    with open("loggin.json", "r") as f:
        for line in f:
            user = json.loads(line.strip())
            if user["username"] == search_username:
                return user["key"]
    return None  

display = ("1.login\n2.signin\n3.exit")
def main():# main fuction is responsible for running everything in the correct order
    while True : 
        print(display)
        user_choice = input("action? :")#asks the user for a choice 
        if user_choice == "1" :#if user chooses option 1... 
            username = input("what is your username? :")#ask user for a username 
            password = input("what is your password? :")#ask user for a password
            if logUser(username,password):#uses log user function to log user in
                ukey = userKey(username) # if it returns true use inputed username to find the users key 
                if ukey:
                    manage_vault(username, ukey)#if we have user key than run manage_vault fuction with username and key
            else:
                print("unable to log in")#if false ask user again
        elif user_choice == "2": # if option 2
            username = input("what is your username? :")#ask user for a username
            while True :
                password = input("what is your password? :")#ask user for a password
                if passwordCheck(password):#run passwordchek fuction if its true
                    print("password is strong")
                    newUser(username,password)#use newUser fuction to add user to the file and stop password check loop
                    break
                else :
                    print("password not strong enough!\nMust contain: 8+ chars, 1 upper, 1 lower, 1 digit, 1 symbol")#else ask the user to input password again
        elif user_choice == "3":#if the user chooses option 3 
            print("goodbye!")
            break#stop the code
if __name__ == "__main__":#ensures that this code can only be run directly
    main()