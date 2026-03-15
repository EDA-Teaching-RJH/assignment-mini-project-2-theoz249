import unittest
from vault import passwordCheck

class testvault(unittest.TestCase):
    def test_weakP(self):
        self.assertFalse(passwordCheck("helloworld"))
    def test_strongP(self):
        self.assertTrue(passwordCheck("He11owwor!d"))
    def test_short_password(self):
        self.assertFalse(passwordCheck("Ab1!"))

if __name__ == "__main__":
    unittest.main()