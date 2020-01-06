from data import object_data

class Object:
    def __init__(self, id, name, desc, states, verbs, moveable):
        self.id = id
        self.name = name
        self.__description = desc
        self.states = states
        self.current_state = next(iter(self.states), None)
        self.verbs = verbs
        self.moveable = moveable
    def __repr__(self):
        return self.name

    @property
    def description(self):
        return self.__description[self.current_state]

    def do_verb(self, verb):
        result = False
        if verb in self.verbs:
            if self.current_state != self.verbs[verb]:
                self.current_state = self.verbs[verb]
                result = True
        return result

    @staticmethod
    def from_id(id):
        if id in object_data:
            return Object(
                id,
                object_data[id]["name"],
                object_data[id]["description"],
                object_data[id]["states"],
                object_data[id]["verbs"],
                object_data[id]["moveable"]
            );
        else:
            return None

    @staticmethod
    def dictionary_from_id_list(ids):
        objects = {}
        for id in ids:
            objects[id] = Object.from_id(id)
        return objects
