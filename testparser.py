import unittest
from parser import Parser

class TestParserMethods(unittest.TestCase):
    def test_directions(self):
        parser = Parser("n")
        self.assertEqual(parser.verb, "go")
        self.assertEqual(parser.noun, "north")
        parser = Parser("south")
        self.assertEqual(parser.verb, "go")
        self.assertEqual(parser.noun, "south")

    def test_two_word_verbs(self):
        parser = Parser("turn on torch")
        self.assertEqual(parser.verb, "turn on")
        self.assertEqual(parser.noun, "torch")
        parser = Parser("ride penny farthing")
        self.assertEqual(parser.verb, "ride")
        self.assertEqual(parser.noun, "pennyfarthing")

    def test_simple_verbs(self):
        parser = Parser("i")
        self.assertEqual(parser.verb, "inventory")
        self.assertEqual(parser.noun, None)
