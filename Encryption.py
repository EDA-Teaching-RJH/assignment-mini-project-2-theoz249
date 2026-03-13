import random
import string
chars= string.ascii_letters+string.punctuation+string.digits+" "+"\t"
chars = list(chars)

def getKey():
    key = chars.copy()
    random.shuffle(key)
    return key

def encrypt(text,key):
    cipher_text = ""
    for letter in text:
        index = chars.index(letter)
        cipher_text += key[index]
    return cipher_text

def decrypt(text,key):
    plain_text = ""
    for letter in text:
        index = key.index(letter)
        plain_text += chars[index]
    return plain_text