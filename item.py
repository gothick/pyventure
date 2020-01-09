class Item:
    def __init__(self, id, data):
        self.id = id
        self.name = data["name"]
        self._description = data["description"]
        # Simple attributes like "is moveable?" etc.
        self.traits = data["traits"]

    @property
    def description(self):
        return self._description
    
    def has_trait(self, trait):
        return trait in self.traits

def __repr__(self):
    return f"{self.name}: {self.description}"

class StatefulItem(Item):
    def __init__(self, id, data):
        super().__init__(id, data)
        self.states = data["states"]
        # Default to the first state in our available states
        self.state = next(iter(self.states), None)
        self.verbs = data["verbs"]

    @property
    def description(self):
        return self._description[self.state]

    def can_verb(self, verb):
        return verb in self.verbs 

    def do_verb(self, verb):
        result = False
        if verb in self.verbs:
            if self.state != self.verbs[verb]:
                self.state = self.verbs[verb]
                result = True
        return result

class ItemFactory:

    @staticmethod
    def create(id, data):
        type = data["type"]
        if type in ItemFactory.choice:
            return ItemFactory.choice[type](id, data)

        assert 0, "Bad item creation: " + type    

    choice = { "Item":  Item,
               "StatefulItem":  StatefulItem                
             }