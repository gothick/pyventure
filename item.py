class Item:
    def __init__(self, id, data):
        self.id = id
        self.name = data["name"]
        self._description = data["description"]
        # Simple attributes like "is moveable?" etc.
        self.traits = data.get("traits") or set()

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

# Very simple Item factory for above items.
class ItemFactory:
    # Create a factory given a dictionary of item data:
    def __init__(self, data):
        self.data = data

    def create_from_id(self, id):
        if id not in self.data:
            raise Exception(f"Could not find item with id '{id}' in item data")
        item_data = self.data[id]
        type = item_data.get("type") or "Item" # Default to the simplest item type
        if type not in ItemFactory.choice:
            raise Exception(f"Unknown item ")
        return ItemFactory.choice[type](id, item_data)

    choice = { 
        "Item":  Item,
        "StatefulItem":  StatefulItem                
    }

    def create_from_id_list(self, ids):
        objects = {}
        for id in ids:
            objects[id] =  self.create_from_id(id)
        return objects