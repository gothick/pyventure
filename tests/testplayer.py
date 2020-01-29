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
    
    def test_combing(self):

        comb = self.item_factory.create_from_noun(Noun.COMB)
        beard_oil = self.item_factory.create_from_noun(Noun.BEARD_OIL)
        self.assertEqual(self.player.beard_status, BeardHealth.STRAGGLY_MESS)
        
        (result, message) = self.player.do_verb(Verb.COMB, Noun.BEARD)
        self.assertFalse(result, "Shouldn't be able to comb if you're not holding a comb")
        
        self.player.give(comb)

        (result, message) = self.player.do_verb(Verb.COMB)
        self.assertFalse(result, "I didn't provide a noun, so what the hell did I just comb?")
        self.assertEqual(message, "Comb what?", "Unexpected message when trying to comb without a noun")

        (result, message) = self.player.do_verb(Verb.COMB, Noun.BOXER_SHORTS)
        self.assertFalse(result, "You should *not* be able to comb your shorts")
        self.assertEqual(message, "You can't comb that.", "Unexpected message when trying to comb without a noun")


        (result, message) = self.player.do_verb(Verb.COMB, Noun.BEARD)
        self.assertTrue(result)
        self.assertEqual(self.player.beard_status, BeardHealth.QUITE_TIDY, "Combing beard without oil should result in QUITE TIDY")
        
        (result, message) = self.player.do_verb(Verb.COMB, Noun.BEARD)
        self.assertFalse(result)
        self.assertEqual(self.player.beard_status, BeardHealth.QUITE_TIDY, "Combing an already tidy beard should change nothing.")
        
        self.player.give(beard_oil)
        (result, message) = self.player.do_verb(Verb.COMB, Noun.BEARD)
        self.assertFalse(result, "Just having the beard oil should make no difference")
        self.assertEqual(self.player.beard_status, BeardHealth.QUITE_TIDY, "Just having the beard oil should make no difference")
        
        self.player.wear(Noun.BEARD_OIL)
        (result, message) = self.player.do_verb(Verb.COMB, Noun.BEARD)
        self.assertTrue(result, "Combing a QUITE TIDY beard while wearing the beard oil should work")
        self.assertEqual(self.player.beard_status, BeardHealth.PERFECTION, "Combing a QUITE TIDY beard while wearing the beard oil should result in PERFECTION")

    def test_riding(self):
        # Something you can't ride
        (result, message) = self.player.do_verb(Verb.RIDE, Noun.BOXER_SHORTS)
        self.assertFalse(result, "Shouldn't be able to ride boxer shorts!")

        # Something you can ride
        bike = self.item_factory.create_from_noun(Noun.PENNY_FARTHING)

        self.assertFalse(self.player.is_riding_anything)

        (result, message) = self.player.do_verb(Verb.RIDE, Noun.PENNY_FARTHING)
        self.assertFalse(result, "Shouldn't be able to ride the bike unless you're holding it.")

        self.player.give(bike)
        (result, message) = self.player.do_verb(Verb.RIDE, Noun.PENNY_FARTHING)
        self.assertTrue(result, "Should be able to ride the bike if you're holding it.")

        (result, message) = self.player.do_verb(Verb.DISMOUNT, Noun.BOXER_SHORTS)
        self.assertFalse(result, "Shouldn't be able to dismount something you're not riding.")

        self.assertTrue(self.player.is_riding_anything)
        self.assertTrue(self.player.is_riding(Noun.PENNY_FARTHING))
        self.assertFalse(self.player.is_riding(Noun.BOXER_SHORTS))

        (item, message) = self.player.take(Noun.PENNY_FARTHING)
        self.assertIsNone(item, "Shouldn't be able to drop something you're riding.")
        
        (result, message) = self.player.do_verb(Verb.DISMOUNT, Noun.PENNY_FARTHING)
        self.assertTrue(result, "Should be able to dismount the bike if you're riding it.")

        self.assertFalse(self.player.is_riding_anything)

        # Shouldn't be able to ride anything twice
        (result, message) = self.player.do_verb(Verb.RIDE, Noun.PENNY_FARTHING)
        (result, message) = self.player.do_verb(Verb.RIDE, Noun.PENNY_FARTHING)
        self.assertFalse(result, "Shouldn't be able to ride more than one thing at once.")

        self.player.do_verb(Verb.DISMOUNT, Noun.PENNY_FARTHING)
        rules = {
            "can_ride": (False, "You can't ride that in here!")
        }
        (result, message) = self.player.do_verb(Verb.RIDE, Noun.PENNY_FARTHING, rules)
        self.assertFalse(result, "Shouldn't be able to ride if prohibited by rules.")
        self.assertEqual(message, "You can't ride that in here!")



