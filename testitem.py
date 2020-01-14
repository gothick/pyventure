import unittest
from item import Item, StatefulItem, ItemFactory

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
        "verbs": { "turn on": "on", "turn off": "off" },
        "traits": { "moveable" }
    },
    "bag": {
        "type": "ContainerItem",
        "name": "Bag of Holding",
        "description": "a bag that can hold many wonders.",
        "inventory": { "shirt", "torch" }
    }
}

class TestParserMethods(unittest.TestCase):
    def setUp(self):
        self.factory = ItemFactory(item_data)

    def test_traitless_item(self):
        item = self.factory.create_from_id("basic")
        self.assertEqual(item.name, "a very basic item")
        self.assertIsInstance(item, Item)

    def test_basic_item(self):
        item = self.factory.create_from_id("shirt")
        self.assertEqual(item.name, "a natty Paisley print shirt")
        self.assertEqual(item.description, "a delightful fitted shirt with a strong Paisley pattern. As you look closely at it your eyes water slightly.")
        self.assertTrue(item.has_trait("moveable"))
        self.assertTrue(item.has_trait("wearable"))

    def test_basic_stateful_item(self):
        item = self.factory.create_from_id("torch")
        self.assertEqual(item.name, "an Ever Ready torch")
        self.assertTrue(item.has_trait("moveable"))
        self.assertFalse(item.has_trait("wearable"))
        
    def test_stateful_item_states(self):
        item = self.factory.create_from_id("torch")
        self.assertTrue(item.can_verb("turn on"))
        self.assertFalse(item.can_verb("whistle"))
        self.assertEqual(item.description, "a plastic 1970s Ever Ready torch. It is switched off.")
        item.do_verb("turn on")
        self.assertEqual(item.description, "a plastic 1970s Ever Ready torch. It's switched on, and emits a surprising amount of light.")
        item.do_verb("turn off")
        self.assertEqual(item.description, "a plastic 1970s Ever Ready torch. It is switched off.")
        item.do_verb("turn off")
        self.assertEqual(item.description, "a plastic 1970s Ever Ready torch. It is switched off.")

    def test_container_item(self):
        item = self.factory.create_from_id("bag")
        self.assertTrue(item.has("shirt"))
        self.assertTrue(item.has("torch"))

    def test_factory(self):
        item = self.factory.create_from_id("torch")
        self.assertIsInstance(item, StatefulItem)
        self.assertEqual(item.name, "an Ever Ready torch")
        self.assertTrue(item.has_trait("moveable"))
        self.assertFalse(item.has_trait("wearable"))


if __name__ == "__main__":
    unittest.main()
