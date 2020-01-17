import unittest
from player import Player, BeardHealth
# TODO we might want to mock the item stuff, or maybe dependency-inject the 
# combing verbs and nouns.
from words import Noun, Verb
from item import ItemFactory
from data import item_data

class TestPlayerMethods(unittest.TestCase):
    def setUp(self):
        self.item_factory = ItemFactory(item_data)

        self.player = Player(
            inventory = {},
            wearing = self.item_factory.create_dictionary_from_nouns([Noun.BOXER_SHORTS]),
            score = 0,
            health = 100, # percent
            caffeine_level = 50 # milligrams
        )
    
    def test_beard(self):
        comb = self.item_factory.create_from_noun(Noun.COMB)
        beard_oil = self.item_factory.create_from_noun(Noun.BEARD_OIL)
        self.assertEqual(self.player.beard_status, BeardHealth.STRAGGLY_MESS)
        
        (result, message) = self.player.do_verb(Verb.COMB)
        self.assertFalse(result)
        
        self.player.give(comb)
        (result, message) = self.player.do_verb(Verb.COMB)
        self.assertTrue(result)
        self.assertEqual(self.player.beard_status, BeardHealth.QUITE_TIDY)
        
        (result, message) = self.player.do_verb(Verb.COMB)
        self.assertFalse(result)
        self.assertEqual(self.player.beard_status, BeardHealth.QUITE_TIDY)
        
        self.player.give(beard_oil)
        (result, message) = self.player.do_verb(Verb.COMB)
        self.assertFalse(result)
        self.assertEqual(self.player.beard_status, BeardHealth.QUITE_TIDY)
        
        self.player.wear(Noun.BEARD_OIL)
        (result, message) = self.player.do_verb(Verb.COMB)
        self.assertTrue(result)
        self.assertEqual(self.player.beard_status, BeardHealth.PERFECTION)
