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
        for k,v in self.exits.items():
            debug += k + ": " + v + "\n"
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

    def room_id_from_exit(self, exit):
        if exit in self.exits:
            return self.exits[exit]
        else:
            return None
