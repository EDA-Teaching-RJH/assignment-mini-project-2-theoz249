import random
import string
chars= string.ascii_letters+string.punctuation+string.digits+" "+"\t"
chars = list(chars)

def getKey():
    key = chars.copy()
    random.shuffle(key)
    return key
