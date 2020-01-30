import textwrap
import random
from item import ItemFactory
from traits import Container
from words import DIRECTIONS
from utility import commalist

class Room(Container):
    def __init__(self, id, item_factory: ItemFactory, data):
        super().__init__(item_factory.create_dictionary_from_nouns(data.get("inventory") or set()))
        self.id = id
        self.name = data["name"]
        self._description = data["description"]
        self.exits = data["exits"]
        self.rules = data.get("rules") or {}

    @property
    def description(self):
        full_desc = self.name + "\n\n"

        d = self._description["basic"]

        for extra in self._description.get("extras") or {}:
            if extra["type"] == "if_in_room":
                if self.has(extra["object"]):
                    d = d + " " + extra["text"]
            if extra["type"] == "random":
                d = d + " " + random.choice(extra["texts"])

        full_desc += d + "\n\n"

        for item in self.inventory.values():
                full_desc += "There is " + item.name + " here.\n"

        if self.exits:
            full_desc += "Exits are " + commalist(list(DIRECTIONS[exit] for exit in self.exits.keys())) + "."
        return full_desc

    def __repr__(self):
        debug = f"Room: {self.name}\n"
        debug += "With exits: \n"
        for id, details in self.exits.items():
            debug += f" {id}\n"
        debug += super().__repr__() 
        return debug

    def can_go(self, exit, player):
        if exit in self.exits:
            rules = self.exits[exit].get("rules")
            if rules:
                for rule in rules:
                    if rule["type"] == "not_if_carrying":
                        if player.has(rule["item"]):
                            return (False, rule["objection"])
                    elif rule["type"] == "not_if_riding":
                        if player.is_riding(rule["item"]):
                            return (False, rule["objection"])
                    else:
                        raise Exception(f"Unknown rule type {rule['type']}")
                return (True, None)
            else:
                return (True, None)

        # Default
        return (False, "You can't go that way.")

    def room_id_from_exit(self, exit):
        if exit in self.exits:
            return self.exits[exit]["destination"]
        else:
            return None

    def transition_from_exit(self, exit):
        if exit in self.exits:
            return self.exits[exit].get("transition")
        else:
            return None
