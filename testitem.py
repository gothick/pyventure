import unittest
from item import Item, StatefulItem, ItemFactory

item_data = {
    "shirt": {
        "type": "Item",
        "name": "a natty Paisley print shirt",
        "description": "a delightful fitted shirt with a strong Paisley pattern. As you look closely at it your eyes water slightly.",
        "verbs": {},
        "traits": { "moveable", "wearable" } 
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
}

class TestParserMethods(unittest.TestCase):
    def test_basic_item(self):
        shirt_data = item_data["shirt"]
        item = Item("shirt", shirt_data)
        self.assertEqual(item.name, "a natty Paisley print shirt")
        self.assertEqual(item.description, "a delightful fitted shirt with a strong Paisley pattern. As you look closely at it your eyes water slightly.")
        self.assertTrue(item.has_trait("moveable"))
        self.assertTrue(item.has_trait("wearable"))

    def test_basic_stateful_item(self):
        torch_data = item_data["torch"]
        item = StatefulItem("torch", torch_data)
        self.assertEqual(item.name, "an Ever Ready torch")
        self.assertTrue(item.has_trait("moveable"))
        self.assertFalse(item.has_trait("wearable"))
        
    def test_stateful_item_states(self):
        torch_data = item_data["torch"]
        item = StatefulItem("torch", torch_data)
        self.assertTrue(item.can_verb("turn on"))
        self.assertFalse(item.can_verb("whistle"))
        self.assertEqual(item.description, "a plastic 1970s Ever Ready torch. It is switched off.")
        item.do_verb("turn on")
        self.assertEqual(item.description, "a plastic 1970s Ever Ready torch. It's switched on, and emits a surprising amount of light.")
        item.do_verb("turn off")
        self.assertEqual(item.description, "a plastic 1970s Ever Ready torch. It is switched off.")
        item.do_verb("turn off")
        self.assertEqual(item.description, "a plastic 1970s Ever Ready torch. It is switched off.")

    def test_factory(self):
        torch_data = item_data["torch"]
        item = ItemFactory.create("torch", torch_data)
        self.assertIsInstance(item, StatefulItem)
        self.assertEqual(item.name, "an Ever Ready torch")
        self.assertTrue(item.has_trait("moveable"))
        self.assertFalse(item.has_trait("wearable"))

if __name__ == "__main__":
    unittest.main()
