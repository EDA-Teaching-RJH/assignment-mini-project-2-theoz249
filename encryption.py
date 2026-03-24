import random
import string
chars= string.ascii_letters+string.punctuation+string.digits+" "+"\t" #creates a variable with different characters
chars = list(chars)#turns it into a list

def getKey():#creates a key that can be used for encryption
    key = chars.copy()#copies chars list into a different variable
    random.shuffle(key)#uses shuffle fucton to randomly shuffle all characters in the list
    key = "".join(key)#changes the format of the list
    return key

def encrypt(text,key):#fuction that encrypts a text using a key
    cipher_text = ""
    for letter in text: # loops for every character in the text#
        index = chars.index(letter)#finds the index of everycharater in text
        cipher_text += key[index]#replaces every character in the text with a character with the same idex from the key list
    return cipher_text

def decrypt(text,key):#fuction that dencrypts a text using a key
    plain_text = ""
    for letter in text:
        index = key.index(letter)
        plain_text += chars[index]
    return plain_text