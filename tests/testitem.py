import unittest
from unittest.mock import patch
from item import Item, StatefulItem, ItemFactory
from random import Random

item_data = {
    "shirt": {
        "type": "Item",
        "name": "a natty Paisley print shirt",
        "description": "a delightful fitted shirt with a strong Paisley pattern. As you look closely at it your eyes water slightly.",
        "traits": { "moveable", "wearable" } 
    },
    "basic": {
        "name": "a very basic item",
        "description": "an item with no traits at all."
    },    
    "torch": {
        "type": "StatefulItem",
        "name": "an Ever Ready torch",
        "description":
        {
            "off": "a plastic 1970s Ever Ready torch. It is switched off.",
            "on": "a plastic 1970s Ever Ready torch. It's switched on, and emits a surprising amount of light."
        },
        "states": [ "off", "on" ],
        "verbs": {
            "turn on": {
                "new_state": "on",
                "message": "You turn on the torch."
            },
            "turn off": {
                "new_state": "off",
                "message": "You turn off the torch."
            }
        },
        "traits": { "moveable" }
    },
    "bag": {
        "type": "ContainerItem",
        "name": "a +100 Bag of Holding",
        "description": "a bag that can hold many wonders.",
        "inventory": { "shirt", "torch" }
    },
    "openstatefulcontainer": {
        "type": "StatefulContainerItem",
        "name": "a stateful container",
        "description": {
            "closed": "a rustic oak cabinet. It is closed.",
            "open": "a rustic oak cabinet. It is open."
        },
        "states": ["open", "closed"],
        "verbs": {
            "open": {
                "new_state": "open",
                "message": "You open the stateful container."
            },
            "close": {
                "new_state": "closed",
                "message": "You close the stateful container."
            }
        },
        "traits": { "moveable" },
        "inventory": {
            "open": { "shirt", "torch" },
            "closed": set()
        }
    },
    "anotherbag": {
        "type": "ContainerItem",
        "name": "another bag",
        "description": "a simple container with a stateful container inside",
        "inventory": { "openstatefulcontainer" }
    },
    "cupboard": {
        "type": "StatefulContainerItem",
        "name": "a rustic oak cabinet",
        "description": {
            "closed": "a cupboard. It is closed.",
            "open": "a cupboard. It is open."
        },
        "states": ["closed", "open"],
        "verbs": {
            "open": {
                "new_state": "open",
                "message": "You open the cubpard."
            },
            "close": {
                "new_state": "closed",
                "message": "You close the cupboard."
            }
        },
        "traits": { "moveable" },
        "inventory": {
            "open": { "shirt", "torch" },
            "closed": set()
        }
    },
    "outercontainer": {
        "type": "ContainerItem",
        "name": "a container",
        "description": "a container with a bag inside",
        "inventory": { "basic", "bag" } 
    },
    "simpleverbable": {
        "type": "SimpleVerbableItem",
        "name": "a simple verbable item.",
        "description": "a simple verbable item with a single, non-random verb result.",
        "verbs": {
            "command": {
                "type": "simple",
                "message": "simple verb message result"
            }
        }
    },
    "simpleverbablerandom": {
        "type": "SimpleVerbableItem",
        "name": "a simple verbable item.",
        "description": "a simple verbable item with a single, non-random verb result.",
        "verbs": {
            "command": {
                "type": "random",
                "messages": [
                    "message0",
                    "message1",
                    "message2"
                ]
            }
        }
    }
}

class TestItemMethods(unittest.TestCase):
    def setUp(self):
        self.factory = ItemFactory(item_data)

    def test_traitless_item(self):
        item = self.factory.create_from_noun("basic")
        self.assertEqual(item.name, "a very basic item")
        self.assertIsInstance(item, Item)

    def test_basic_item(self):
        item = self.factory.create_from_noun("shirt")
        self.assertEqual(item.name, "a natty Paisley print shirt")
        self.assertEqual(item.description, "a delightful fitted shirt with a strong Paisley pattern. As you look closely at it your eyes water slightly.")
        self.assertTrue(item.has_trait("moveable"))
        self.assertTrue(item.has_trait("wearable"))

    def test_basic_stateful_item(self):
        item = self.factory.create_from_noun("torch")
        self.assertEqual(item.name, "an Ever Ready torch")
        self.assertTrue(item.has_trait("moveable"))
        self.assertFalse(item.has_trait("wearable"))

    def test_state_change_returns(self):
        item = self.factory.create_from_noun("torch")
        (result, message) = item.do_verb("turn off")
        self.assertFalse(result, "Turning off a turned off item unexpectedly did something.")
        (result, message) = item.do_verb("turn on")
        self.assertTrue(result, "Could not turn on a turned off item.")
        self.assertEqual(message, "You turn on the torch.", "Wrong message when turning on item.")
        (result, message) = item.do_verb("turn off")
        self.assertTrue(result, "Could not turn off a turned on item.")
        self.assertEqual(message, "You turn off the torch.", "Wrong message when turning off item.")
        
    def test_stateful_item_states(self):
        item = self.factory.create_from_noun("torch")
        
        (result, message) = item.do_verb("turn on")
        self.assertTrue(result, "You should be able to turn on a torch.")
        (result, message) = item.do_verb("turn off")
        self.assertTrue(result, "You should be able to turn off a torch.")

        (result, message) = item.do_verb("throw")
        self.assertFalse(result, "Shouln't be able to throw the torch.")
        self.assertEqual(message, "You can't do that.", "Wrong failure message when throwing torch.")
        
        self.assertEqual(item.description, "a plastic 1970s Ever Ready torch. It is switched off.")
        item.do_verb("turn on")
        self.assertEqual(item.description, "a plastic 1970s Ever Ready torch. It's switched on, and emits a surprising amount of light.")
        item.do_verb("turn off")
        self.assertEqual(item.description, "a plastic 1970s Ever Ready torch. It is switched off.")
        item.do_verb("turn off")
        self.assertEqual(item.description, "a plastic 1970s Ever Ready torch. It is switched off.")

    def test_simple_verbable_item(self):
        item = self.factory.create_from_noun("simpleverbable")
        (result, message) = item.do_verb("flobble")
        self.assertFalse(result, "Shouldn't be able to flobble a SimpleVerbableItem")
        (result, message) = item.do_verb("command")
        self.assertTrue(result, "Should be able to command a SimpleVerbableItem.")
        self.assertEqual(message, "simple verb message result", "Wrong command result from SimpleVerbableItem")

    @patch('item.random')
    def test_simple_verbable_item_with_random_result(self, random):
        # https://stackoverflow.com/questions/26091330/how-to-validate-a-unit-test-with-random-values
        # Seed a patched random number generator
        my_random = Random(123)
        random.choice._mock_side_effect = my_random.choice

        item = self.factory.create_from_noun("simpleverbablerandom")
        (result, message) = item.do_verb("flobble")
        self.assertFalse(result, "Shouldn't be able to flobble a SimpleVerbableItem")
        (result, message) = item.do_verb("command")
        self.assertTrue(result, "Should be able to command a SimpleVerbableItem.")

        # This is the order our seed guarantees:
        self.assertEqual(message, "message0", "Wrong command result from SimpleVerbableItem")
        (result, message) = item.do_verb("command")
        self.assertEqual(message, "message1", "Wrong command result from SimpleVerbableItem")
        (result, message) = item.do_verb("command")
        self.assertEqual(message, "message0", "Wrong command result from SimpleVerbableItem")
        (result, message) = item.do_verb("command")
        self.assertEqual(message, "message1", "Wrong command result from SimpleVerbableItem")
        (result, message) = item.do_verb("command")
        self.assertEqual(message, "message1", "Wrong command result from SimpleVerbableItem")
        (result, message) = item.do_verb("command")
        self.assertEqual(message, "message0", "Wrong command result from SimpleVerbableItem")
        (result, message) = item.do_verb("command")
        self.assertEqual(message, "message0", "Wrong command result from SimpleVerbableItem")
        (result, message) = item.do_verb("command")
        self.assertEqual(message, "message1", "Wrong command result from SimpleVerbableItem")
        (result, message) = item.do_verb("command")
        self.assertEqual(message, "message2", "Wrong command result from SimpleVerbableItem")
        (result, message) = item.do_verb("command")
        self.assertEqual(message, "message2", "Wrong command result from SimpleVerbableItem")
        

    def test_container_item(self):
        item = self.factory.create_from_noun("bag")
        self.assertTrue(item.has("shirt"))
        self.assertTrue(item.has("torch"))

    def test_stateful_container_item(self):
        item = self.factory.create_from_noun("cupboard")
        self.assertFalse(item.has("shirt"))
        self.assertFalse(item.has("torch"))
        item.do_verb("open")
        self.assertTrue(item.has("shirt"))
        self.assertTrue(item.has("torch"))

    def test_recursive_take(self):
        container = self.factory.create_from_noun("outercontainer")
        self.assertTrue(container.has("bag"))
        self.assertTrue(container.has("shirt"))
        self.assertTrue(container.has("torch"))

        self.assertIsNotNone(container.take("torch"))
        self.assertIsNotNone(container.take("shirt"))
        self.assertIsNotNone(container.take("bag"))

    def test_recursive_get_item_reference(self):
        container = self.factory.create_from_noun("outercontainer")

        bag = container.get_item_reference("bag")
        self.assertIsNotNone(bag, "Could not get bag from inside container")
        self.assertEqual(bag.id, "bag")

        shirt = container.get_item_reference("shirt")
        self.assertIsNotNone(shirt, "Could not get shirt from inside bag inside container")
        self.assertEqual(shirt.id, "shirt")

        torch = container.get_item_reference("torch")
        self.assertIsNotNone(torch, "Could not get torch from inside bag inside container")
        self.assertEqual(torch.id, "torch")

    def test_recursive_stateful_container(self):
        anotherbag = self.factory.create_from_noun("anotherbag")
        self.assertTrue(anotherbag.has("shirt"))

    def test_factory(self):
        item = self.factory.create_from_noun("torch")
        self.assertIsInstance(item, StatefulItem)
        self.assertEqual(item.name, "an Ever Ready torch")
        self.assertTrue(item.has_trait("moveable"))
        self.assertFalse(item.has_trait("wearable"))


if __name__ == "__main__":
    unittest.main()
