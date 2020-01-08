import textwrap
from object import Object

class Room:
    def __init__(self, id, name, description, objects, exits, states):
        self.id = id
        self.name = name
        self.description = description
        self.states = states
        self.objects = {}
        for state, inventory in objects.items():
            self.objects[state] = Object.dictionary_from_id_list(inventory)
        self.exits = exits
        self.current_state = next(iter(self.states), None)

    def full_description(self, wrap_width):
        full_desc = self.name + "\n\n"

        d = self.description[self.current_state]

        if "extras" in self.description:
            for extra in self.description["extras"]:
                if extra["type"] == "if_in_room":
                    if self.has(extra["object"]):
                        d = d + extra["text"]

        full_desc += textwrap.fill(d, wrap_width) + "\n\n"

        objects = self.objects[self.current_state]

        if (objects):
            for o in objects.values():
                full_desc += "There is " + o.name + " here.\n"

        if self.exits:
            full_desc += "Exits are " + ", ".join(self.exits.keys())
        return full_desc


    def __repr__(self):
        debug = self.name + "\n"
        debug += "With exits: \n"
        if len(self.exits):
            for id, details in self.exits.items():
                debug += f" {id}\n"
        debug += f"in state {self.current_state}\n"
        if len(self.objects[self.current_state]) > 0:
            debug += "with objects: \n"
            for object in self.objects[self.current_state].values():
                debug += f" {object.name}\n"
        return debug

    def has(self, object_id):
        return object_id in self.objects[self.current_state]

    def get(self, object_id):
        return self.objects[self.current_state].get(object_id)

    def take(self, object_id):
        objects = self.objects[self.current_state]

        if objects[object_id].moveable:
            return objects.pop(object_id)
        else:
            return None

    def add_object(self, object):
        self.objects[self.current_state][object.id] = object

    def can_go(self, exit, player):
        if exit in self.exits:
            rules = self.exits[exit].get("rules")
            if rules:
                for rule in rules:
                    if rule["type"] == "not_if_carrying":
                        if player.is_carrying(rule["object"]):
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
