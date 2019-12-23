import textwrap
from object import Object

class Room:
    def __init__(self, id, name, description, objects, exits, states):
        self.id = id
        self.name = name
        self.description = description
        self.states = states
        if self.states:
            self.objects = {} 
            for state, inventory in objects.items():
                self.objects[state] = Object.dictionary_from_id_list(inventory)
        else:
            self.objects = Object.dictionary_from_id_list(objects)
        self.exits = exits
        self.current_state = next(iter(self.states), None)

    def full_description(self, wrap_width):
        full_desc = self.name + "\n"
        
        if self.current_state:
            d = self.description[self.current_state]
        else:
            d = self.description

        full_desc += textwrap.fill(d, wrap_width) + "\n"

        if self.current_state:
            objects = self.objects[self.current_state]
        else:
            objects = self.objects
        
        if (objects):
            for o in objects.values():
                full_desc += "There is " + o.name + " here\n"
        return full_desc

    def __repr__(self):
        debug = self.name + "\n"
        debug += "With exits: \n"
        for k,v in self.exits.items():
            debug += k + ": " + v + "\n"
        return debug

    def has(self, object_id):
        if self.current_state:
            return object_id in self.objects[self.current_state]
        return object_id in self.objects

    def take(self, object_id):
        if self.current_state:
            return self.objects[self.current_state].pop(object_id)
        return self.objects.pop(object_id)

    def add_object(self, object):
        if self.current_state:
            self.objects[self.current_state][object.id] = object
        else:
            self.objects[object.id] = object

    def room_id_from_exit(self, exit):
        if exit in self.exits:
            return self.exits[exit]
        else:
            return None

