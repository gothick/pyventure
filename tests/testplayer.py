import unittest
from player import Player, BeardHealth
# TODO we might want to mock the item stuff, or maybe dependency-inject the 
# combing verbs and nouns.
from words import Noun, Verb
from item import ItemFactory
from data import item_data
from unittest.mock import Mock


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

    def test_basic_wearing(self):
        self.assertFalse(self.player.has_top_on)
        self.assertFalse(self.player.has_bottom_on)
        
        # These trousers aren't wearable:
        attrs = {
            'has_trait.return_value': False,
            'get_trait.return_value': None
        }
        trousers = Mock(id="trousers", name="trousers", **attrs)

        self.player.give(trousers)
        (result, message) = self.player.wear("trousers")
        self.assertFalse(result, "Should not be able to wear an item with no wearable trait")
        self.assertEqual(message, "You can't wear that.", "Unexpected message from wear failure")

        # This shirt is wearable and moveable
        def has_trait(trait):
            return trait in ("wearable", "moveable")
        def get_trait(trait):
            return {} if trait in ("wearable", "moveable") else None

        attrs = {
            'has_trait.side_effect': has_trait,
            'get_trait.side_effect': get_trait
        }
        shirt = Mock(id = "shirt", name="shirt", **attrs)

        self.player.give(shirt)
        (result, message) = self.player.wear("shirt")
        self.assertTrue(result, f"Should be able to wear a basic wearable item. Message was: {message}")
    
    def test_wearing_tops(self):
        # Two wearable, moveable tops:
        def has_trait(trait):
            return trait in ("wearable", "moveable", "top")
        def get_trait(trait):
            return {} if trait in ("wearable", "moveable", "top") else None

        attrs = {
            'has_trait.side_effect': has_trait,
            'get_trait.side_effect': get_trait
        }
        shirt1 = Mock(id = "shirt1", name="shirt one", **attrs)
        shirt2 = Mock(id = "shirt2", name="shirt two", **attrs)

        self.player.give(shirt1)
        self.player.give(shirt2)

        (result, message) = self.player.wear("shirt1")
        self.assertTrue(result, f"Should be able to wear one top. Failure message was: {message}")
        
        (result, message) = self.player.wear("shirt2")
        self.assertFalse(result, f"Should not be able to wear two tops. Unexpected success message was: {message}")
        self.assertIn("take something off", message, "Failure message on trying to wear two shirts should include correct advice.")
        

    def test_wearing_bottoms(self):
        # Two wearable, moveable bottoms:
        def has_trait(trait):
            return trait in ("wearable", "moveable", "bottom")
        def get_trait(trait):
            return {} if trait in ("wearable", "moveable", "bottom") else None

        attrs = {
            'has_trait.side_effect': has_trait,
            'get_trait.side_effect': get_trait
        }
        trousers1 = Mock(id = "trousers1", **attrs)
        # Workaround because Mock itself has an annoying name attribute! https://docs.python.org/3/library/unittest.mock.html#mock-names-and-the-name-attribute
        trousers1.configure_mock(name = "trousers1")
        trousers2 = Mock(id = "trousers2", name="trousers two", **attrs)
        # Workaround because Mock itself has an annoying name attribute! https://docs.python.org/3/library/unittest.mock.html#mock-names-and-the-name-attribute
        trousers2.configure_mock(name = "trousers2")

        self.player.give(trousers1)
        self.player.give(trousers2)

        (result, message) = self.player.wear("trousers1")
        self.assertTrue(result, f"Should be able to wear one set of bottoms. Failure message was: {message}")
        
        (result, message) = self.player.wear("trousers2")
        self.assertFalse(result, f"Should not be able to wear two sets of bottoms. Unexpected success message was: {message}")
        self.assertIn("take something off", message, "Failure message on trying to wear two pairs of trousers should include correct advice.")
        
    def test_wearing_status(self):
        # Top
        def has_trait_top(trait):
            return trait in ("wearable", "moveable", "top")
        def get_trait_top(trait):
            return {} if trait in ("wearable", "moveable", "top") else None

        attrs = {
            'has_trait.side_effect': has_trait_top,
            'get_trait.side_effect': get_trait_top
        }
        shirt = Mock(id = "shirt", **attrs)
        # Workaround because Mock itself has an annoying name attribute! https://docs.python.org/3/library/unittest.mock.html#mock-names-and-the-name-attribute
        shirt.configure_mock(name = "shirt")

        # Bottoms
        def has_trait_bottom(trait):
            return trait in ("wearable", "moveable", "bottom")
        def get_trait_bottom(trait):
            return {} if trait in ("wearable", "moveable", "bottom") else None

        attrs = {
            'has_trait.side_effect': has_trait_bottom,
            'get_trait.side_effect': get_trait_bottom
        }
        trousers = Mock(id = "trousers", **attrs)
        # Workaround because Mock itself has an annoying name attribute! https://docs.python.org/3/library/unittest.mock.html#mock-names-and-the-name-attribute
        trousers.configure_mock(name = "trousers")

        self.player.give(shirt)
        self.player.give(trousers)

        # Basics
        self.assertTrue(self.player.is_wearing(Noun.BOXER_SHORTS), "Test player should start with boxers on")
        self.assertFalse(self.player.is_wearing("didgeridoo"), "is_wearing should not be true for an arbitrary didgeridoo")

        self.assertFalse(self.player.has_bottom_on)
        self.assertFalse(self.player.has_top_on)
        self.assertFalse(self.player.is_fully_clothed)
        
        # Add a top and re-test
        self.player.wear("shirt")
        self.assertTrue(self.player.has_top_on)
        self.assertFalse(self.player.has_bottom_on)
        self.assertEqual(self.player.current_top, shirt)
        self.assertIsNone(self.player.current_bottom)
        self.assertFalse(self.player.is_fully_clothed)

        # Add trousers
        self.player.wear("trousers")
        self.assertTrue(self.player.has_top_on)
        self.assertTrue(self.player.has_bottom_on)
        self.assertEqual(self.player.current_top, shirt)
        self.assertEqual(self.player.current_bottom, trousers)
        self.assertTrue(self.player.is_fully_clothed)

        self.player.unwear("trousers")
        self.assertFalse(self.player.has_bottom_on)
        self.player.unwear("shirt")
        self.assertFalse(self.player.has_top_on)