import encryption
import json
import re
import string

try:
    with open("loggin.json", "r") as f:
        print("File exists and is readable.")
except FileNotFoundError:
    with open("loggin.json", "w") as f:  
        pass
    print("file created")
except IOError:
    print("Could not access or create the file.")
    pass

username = ""
password = ""
personalkey = ""

def newUser(username,password):
    personalkey = encryption.getKey()
    password = encryption.encrypt(password, personalkey)
    user_data = {
        "username": username,
        "password": password,
        "key": personalkey
    }
    with open("loggin.json", "a", newline = '') as f:
        f.write(json.dumps(user_data) + "\n")
    print("Account created successfully!")



def logUser(username, password):
    try:
        with open("loggin.json", "r") as f:
            for line in f:
                user = json.loads(line)
                if user["username"] == username:
                    decrypted_password = encryption.decrypt(user["password"], user["key"])
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

def manage_vault(username, key):
    filename = f"vault_{username}.json"
    try:
        with open(filename, "r") as f:
            encrypted_items = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(filename,"w") as f:
            pass
        encrypted_items = []
    while True:
        print(f"\n--- {username.uper()}'S VAULT ---")
        print(f"Total secrets: {len(encrypted_items)}")
        choice = input("1. Add secret\n2. View/Remove Secrets\n3. Logout\n: ")
        if choice == "1":
            secret = input("Enter secret to store: ")
            enc_secret = encryption.encrypt(secret, key)
            encrypted_items.append(enc_secret)
            with open(filename, "w") as f:
                json.dump(encrypted_items, f)
            print("Secret encrypted and added.")
        elif choice == "2":
            if not encrypted_items:
                print("Vault is empty.")
                continue
            print("\n--- Your Secrets ---")
            for i, enc_val in enumerate(encrypted_items):
                decrypted = encryption.decrypt(enc_val,key)
                print(f"{i+1}.{decrypted}")
            rem = input("\nRemove # (or 'b' to go back): ")
            if rem.lower() == "b":
                continue
            elif rem.isdigit():
                idx = int(rem) - 1
                if 0 <= idx < len(encrypted_items):
                    encrypted_items.pop(idx)
                    with open(filename, "w") as f:
                        json.dump(encrypted_items, f)
                    print(f"Successfully removed item #{rem}")
                else:
                    print("Invalid number. No item removed.")
        elif choice == "3":
            print("Vault saved and locked.")
            break


def userKey(search_username):
    with open("loggin.json", "r") as f:
        for line in f:
            user = json.loads(line.strip())
            if user["username"] == search_username:
                return user["key"]
    return None             

display = ("1.login\n2.signin\n3.exit")
def main():
    while True : 
        print(display)
        user_choice = input("action? :")
        if user_choice == "1" :
            username = input("what is your username? :")
            password = input("what is your password? :")
            if logUser(username,password):
                ukey = userKey(username)
                if ukey:
                    manage_vault(username, ukey)
            else:
                print("unable to log in")
        elif user_choice == "2":
            username = input("what is your username? :")
            while True :
                password = input("what is your password? :")
                if passwordCheck(password):
                    print("password is strong")
                    newUser(username,password)
                    break
                else :
                    print("password not strong enough!\nMust contain: 8+ chars, 1 upper, 1 lower, 1 digit, 1 symbol")
        elif user_choice == "3":
            print("goodbye!")
            break

main()