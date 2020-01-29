import unittest
from unittest.mock import Mock
# TODO Mock items and factory?
from item import Item, ItemFactory
from room import Room
from words import DIRECTIONS
from words import Noun

item_data = {
    "bike": {
        "type": "Item",
        "name": "a bike",
        "description": "a bike.",
        "traits": { "moveable", "wearable" } 
    },
    "simple_item": {
        "name": "a simple item",
        "description": "a simple item."
    }
}

room_data = {
    "simpleroom": {
        "name": "Simple Room",
        "description": {
            "basic": "Basic description"
        },
        "exits": {
            Noun.SOUTH: {
                "destination": "livingroom"
            }
        }
    },
    "livingroom": {
        "name": "The Living Room",
        "inventory": [ "bike", "simple_item" ],
        "rules": {
            "can_ride": (False, "You can't ride that in here!")
        },
        "description": {
            "basic":  "A living room.",
            "extras": [
                {
                    "type": "if_in_room",
                    "object": "bike",
                    "text": "By the front door rests a bike."
                }
            ]
        },
        "exits": {
            Noun.NORTH: {
                "destination": "simpleroom",
                "transition": "Northerly transition",
                "rules": [
                    {
                        "type": "not_if_riding",
                        "item": "bike",
                        "objection": "You can't ride that thorugh there."
                    },
                    {
                        "type": "not_if_carrying",
                        "item": "simple_item",
                        "objection": "You can't carry that through there."
                    }
                ]
            }
        }
    },
}

class TestRoomMethods(unittest.TestCase):
    def setUp(self):
        self.item_factory = ItemFactory(item_data)
        self.rooms = {}

        # Build our little universe.
        for id, data in room_data.items():
            self.rooms[id] = Room(id, self.item_factory, data)

    def test_basic_exits(self):
        room = self.rooms["simpleroom"]
        player = Mock()
        (result, _) = room.can_go(Noun.NORTH, player)
        self.assertFalse(result, "Shouldn't be able to go north when that exit doesn't exist")

        (result, _) = room.can_go(Noun.SOUTH, player)
        self.assertTrue(result, "Should be able to exit south")

        self.assertEqual(room.room_id_from_exit(Noun.SOUTH), "livingroom")
        self.assertEqual(room.room_id_from_exit(Noun.WEST), None)

        room = self.rooms["livingroom"]
        self.assertEqual(room.transition_from_exit(Noun.NORTH), "Northerly transition")
        self.assertEqual(room.transition_from_exit(Noun.SOUTH), None)


    def test_can_go_conditions(self):
        room = self.rooms["livingroom"]
        attrs = {
            'is_riding.return_value': False,
            'has.return_value': False
        }
        player = Mock(**attrs)
        (result, _) = room.can_go(Noun.NORTH, player)
        self.assertTrue(result, "Basic player should be able to go north unimpeded")

        attrs = {
            'is_riding.return_value': True,
            'has.return_value': False
        }
        player = Mock(**attrs)
        (result, message) = room.can_go(Noun.NORTH, player)
        self.assertFalse(result, "Player riding a bike should be impeded by rule")

        attrs = {
            'is_riding.return_value': False,
            'has.return_value': True
        }
        player = Mock(**attrs)
        (result, message) = room.can_go(Noun.NORTH, player)
        self.assertFalse(result, "Player carrying something be impeded by rule")
    
    def test_description(self):
        room = self.rooms["simpleroom"]
        desc = room.description
        self.assertIn("Basic description", desc, "Room's description attribute doesn't contain its basic description")
        self.assertIn("south", desc, "Room's description attribute doesn't contain a known exit")

        room = self.rooms["livingroom"]
        desc = room.description
        self.assertIn("There is a bike here", desc, "Inventory item not listed in room description")
        self.assertIn("By the front door rests a bike", desc, "Room extra wasn't present in description")
        room.take("bike")
        desc = room.description
        self.assertNotIn("By the front door rests a bike", desc, "Conditional room extra doesn't disappear when item removed")


    def test_can_go(self):
        pass
        
if __name__ == "__main__":
    unittest.main()
