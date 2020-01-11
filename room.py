import textwrap
from item import ItemFactory
class Room:
    def __init__(self, id, item_factory: ItemFactory, data):
        self.id = id
        self.name = data["name"]
        self.description = data["description"]
        self.inventory = item_factory.create_from_id_list(data.get("inventory") or set())
        self.exits = data["exits"]

    def full_description(self, wrap_width):
        full_desc = self.name + "\n\n"

        d = self.description["basic"]

        for extra in self.description.get("extras") or {}:
            if extra["type"] == "if_in_room":
                if self.has(extra["object"]):
                    d = d + extra["text"]

        full_desc += textwrap.fill(d, wrap_width) + "\n\n"

        for item in self.inventory.values():
                full_desc += "There is " + item.name + " here.\n"

        if self.exits:
            full_desc += "Exits are " + ", ".join(self.exits.keys())
        return full_desc

    def __repr__(self):
        debug = self.name + "\n"
        debug += "With exits: \n"
        for id, details in self.exits.items():
            debug += f" {id}\n"
        if self.inventory:
            debug += "with inventory: \n"
            for item in self.inventory.values():
                debug += f" {item.name}\n"
        return debug

    def has(self, item_id):
        return item_id in self.inventory

    def get_item_reference(self, item_id):
        return self.inventory.get(item_id)

    def take(self, item_id):
        if self.inventory[item_id].has_trait("moveable"):
            return self.inventory.pop(item_id)
        else:
            return None

    def add_item(self, item):
        self.inventory[item.id] = item

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
