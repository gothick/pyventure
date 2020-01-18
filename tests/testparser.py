import unittest
from parser import Parser
from enum import Enum, auto

# test data
class Noun(Enum):
    DOODAH = auto()
    # Directions
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()
    UP = auto()
    DOWN = auto()
    # Items
    UNKNOWN = auto() # Represents a noun that's not in our vocabulary
    TORCH = auto()
    PHONE = auto()
    TV = auto()
    PENNY_FARTHING = auto()
    PLUS_FOURS = auto()

DIRECTIONS = [ Noun.NORTH, Noun.EAST, Noun.SOUTH, Noun.WEST, Noun.UP, Noun.DOWN ]

normalised_nouns = {
    "north": Noun.NORTH,
    "n": Noun.NORTH,
    "east": Noun.EAST,
    "e": Noun.EAST,
    "south": Noun.SOUTH,
    "s": Noun.SOUTH,
    "west": Noun.WEST,
    "w": Noun.WEST,
    "up": Noun.UP,
    "u": Noun.UP,
    "down": Noun.DOWN,
    "d": Noun.DOWN,

    "iphone": Noun.PHONE,
    "iphone se": Noun.PHONE,
    "phone": Noun.PHONE,    
    "pennyfarthing": Noun.PENNY_FARTHING,
    "penny farthing": Noun.PENNY_FARTHING,
    "penny-farthing": Noun.PENNY_FARTHING,

    "plus fours": Noun.PLUS_FOURS,
    "plus-fours": Noun.PLUS_FOURS
}


class Verb(Enum):
    RIDE = auto()
    TURN_ON = auto()
    TURN_OFF = auto()
    GO = auto()
    EXAMINE = auto()
    TAKE = auto(),
    INVENTORY = auto(),
    WEAR = auto()

normalised_verbs = {
    "ride": Verb.RIDE,
    "get on": Verb.RIDE,
    "turn on": Verb.TURN_ON,
    "activate": Verb.TURN_ON,
    "turn off": Verb.TURN_OFF,
    "deactivate": Verb.TURN_OFF,
    "inventory": Verb.INVENTORY,
    "i": Verb.INVENTORY,
    "look": Verb.EXAMINE,
    "examine": Verb.EXAMINE,
    "wear": Verb.WEAR,
    "put on": Verb.WEAR
}


class TestParserMethods(unittest.TestCase):
    def setUp(self):
        self.parser = Parser(
            Noun,
            Noun.UNKNOWN, 
            Verb,
            Verb.GO,
            DIRECTIONS,
            normalised_nouns,
            normalised_verbs
        )

    def test_directions(self):
        self.parser.parse("n")
        self.assertEqual(self.parser.verb, Verb.GO)
        self.assertEqual(self.parser.noun, Noun.NORTH)

        self.parser.parse("south")
        self.assertEqual(self.parser.verb, Verb.GO)
        self.assertEqual(self.parser.noun, Noun.SOUTH)

    def test_article_stripping(self):
        self.parser.parse("turn on the iphone")
        self.assertEqual(self.parser.verb, Verb.TURN_ON)
        self.assertEqual(self.parser.noun, Noun.PHONE)
        
        self.parser.parse("examine a penny farthing")
        self.assertEqual(self.parser.verb, Verb.EXAMINE)
        self.assertEqual(self.parser.noun, Noun.PENNY_FARTHING)
        

    def test_two_word_verbs(self):
        self.parser.parse("turn on iphone")
        self.assertEqual(self.parser.verb, Verb.TURN_ON)
        self.assertEqual(self.parser.noun, Noun.PHONE)
        
        self.parser.parse("examine iphone")
        self.assertEqual(self.parser.verb, Verb.EXAMINE)
        self.assertEqual(self.parser.noun, Noun.PHONE)
        
        self.parser.parse("ride penny farthing")
        self.assertEqual(self.parser.verb, Verb.RIDE)
        self.assertEqual(self.parser.noun, Noun.PENNY_FARTHING)

    def test_two_word_verbs_with_two_word_nouns(self):
        self.parser.parse("put on plus fours")
        self.assertEqual(self.parser.verb, Verb.WEAR, "Expected 'put on plus fours' to yield Verb.WEAR")
        self.assertEqual(self.parser.noun, Noun.PLUS_FOURS, "Expected 'put on plus fours to yield Noun.PLUS_FOURS")

    def test_simple_verbs(self):
        self.parser.parse("i")
        self.assertEqual(self.parser.verb, Verb.INVENTORY)
        self.assertEqual(self.parser.noun, None)
        self.parser.parse("look")
        self.assertEqual(self.parser.verb, Verb.EXAMINE)
        self.assertEqual(self.parser.noun, None)

if __name__ == "__main__":
    unittest.main()
