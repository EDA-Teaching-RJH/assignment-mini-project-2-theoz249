import unittest
from vault import passwordCheck

class testvault(unittest.TestCase):
    def test_weakP(self):
        self.assertFalse(passwordCheck("helloworld"))#tests to see if the result for this password is false 
    def test_strongP(self):
        self.assertTrue(passwordCheck("He11owwor!d"))#same thing but result shuld be true 
    def test_short_password(self):
        self.assertFalse(passwordCheck("Ab1!"))#also tests if the password lenght works

if __name__ == "__main__":
    unittest.main()