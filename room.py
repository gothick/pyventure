import textwrap
import random
from item import ItemFactory
from traits import Container
from words import DIRECTIONS


class Room(Container):
    def __init__(self, id, item_factory: ItemFactory, data):
        super().__init__(item_factory.create_dictionary_from_nouns(data.get("inventory") or set()))
        self.id = id
        self.name = data["name"]
        self.description = data["description"]
        self.exits = data["exits"]

    def full_description(self, wrap_width):
        full_desc = self.name + "\n\n"

        d = self.description["basic"]

        for extra in self.description.get("extras") or {}:
            if extra["type"] == "if_in_room":
                if self.has(extra["object"]):
                    d = d + " " + extra["text"]
            if extra["type"] == "random":
                d = d + " " + random.choice(extra["texts"])

        full_desc += textwrap.fill(d, wrap_width) + "\n\n"

        for item in self.inventory.values():
                full_desc += "There is " + item.name + " here.\n"

        if self.exits:
            full_desc += "Exits are " + ", ".join(DIRECTIONS[exit] for exit in self.exits.keys()) + "."
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
                        else:
                            return (True, None)
                    else:
                        raise Exception(f"Unknown rule type {rule['type']}")
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
