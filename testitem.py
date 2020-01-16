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
            "open": "open",
            "close": "closed"
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
            "closed": "a rustic oak cabinet. It is closed.",
            "open": "a rustic oak cabinet. It is open."
        },
        "states": ["closed", "open"],
        "verbs": { 
            "open": "open",
            "close": "closed"
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
    }
}

class TestItemMethods(unittest.TestCase):
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

    def test_stateful_container_item(self):
        item = self.factory.create_from_id("cupboard")
        self.assertFalse(item.has("shirt"))
        self.assertFalse(item.has("torch"))
        item.do_verb("open")
        self.assertTrue(item.has("shirt"))
        self.assertTrue(item.has("torch"))

    def test_recursive_take(self):
        container = self.factory.create_from_id("outercontainer")
        self.assertTrue(container.has("bag"))
        self.assertTrue(container.has("shirt"))
        self.assertTrue(container.has("torch"))

        self.assertIsNotNone(container.take("torch"))
        self.assertIsNotNone(container.take("shirt"))
        self.assertIsNotNone(container.take("bag"))

    def test_recursive_get_item_reference(self):
        container = self.factory.create_from_id("outercontainer")

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
        anotherbag = self.factory.create_from_id("anotherbag")
        self.assertTrue(anotherbag.has("shirt"))

    def test_factory(self):
        item = self.factory.create_from_id("torch")
        self.assertIsInstance(item, StatefulItem)
        self.assertEqual(item.name, "an Ever Ready torch")
        self.assertTrue(item.has_trait("moveable"))
        self.assertFalse(item.has_trait("wearable"))


if __name__ == "__main__":
    unittest.main()
