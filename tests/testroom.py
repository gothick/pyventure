import unittest
from unittest.mock import Mock
# TODO Mock items and factory?
from item import Item, ItemFactory
from room import Room

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
            "south": {
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
            "north": {
                "destination": "simpleroom",
                "rules": [
                    {
                        # We don't want to let the player carry the penny-farthing into
                        # the house. 
                        "type": "not_if_carrying",
                        "item": "bike",
                        "objection": "The penny-farthing won't fit through there."
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

        # Build the universe.
        for id, data in room_data.items():
            self.rooms[id] = Room(id, self.item_factory, data)

    def test_description(self):
        room = self.rooms["simpleroom"]
        player = Mock()
        (result, _) = room.can_go("north", player)
        self.assertFalse(result, "Shouldn't be able to go north when that exit doesn't exist")

    def test_can_go(self):
        pass
        
if __name__ == "__main__":
    unittest.main()
