import unittest
from vault import passwordCheck

class testvault(unittest.TestCase):
    def test_weakP(self):
        self.assertFalse(passwordCheck("helloworld"))
    def test_strongP(self):
        self.assertTrue(passwordCheck("He11owwor!d"))