# Very simple Item factory.
class ItemFactory:
    # Create a factory given a dictionary of item data:
    def __init__(self, data):
        self.data = data

    def create_from_id(self, id):
        if id not in self.data:
            raise Exception(f"Could not find item with id '{id}' in item data")
        item_data = self.data[id]
        type = item_data.get("type") or "Item" # Default to the simplest item type
        cls = globals()[type]
        if not cls:
            raise Exception(f"Unknown item type: {type}")
        return cls(id, item_data, self)

    def create_from_id_list(self, ids):
        objects = {}
        for id in ids:
            objects[id] =  self.create_from_id(id)
        return objects

# The actual Item classes
class Item:
    def __init__(self, id, data, item_factory):
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

    # A basic item cannot contain anything. Subclasses that 
    # contain things can override this. Implementing it here
    # means that we can recurse through a hierarchy of objects
    # looking for things and this will terminate the search.
    def has(self, _):
        return False

def __repr__(self):
    return f"{self.name}: {self.description}"

class StatefulItem(Item):
    def __init__(self, id, data, item_factory):
        super().__init__(id, data, item_factory)
        assert(data["states"])
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

class ContainerItem(Item):
    def __init__(self, id, data, item_factory):
        super().__init__(id, data, item_factory)
        self.inventory = item_factory.create_from_id_list(data["inventory"])

    @property
    def description(self):
        d = self._description
        if len(self.inventory) == 1:
            d += " It contains " + next(iter(self.inventory.values)).name + "."
        elif len(self.inventory) > 1:
            names = list(i.name for i in self.inventory.values())
            d += " It contains " + "{} and {}".format(", ".join(names[:-1]),  names[-1]) + "."
        return d

    def has(self, find_item_id):
        for (item_id, item) in self.inventory.items():
            if item_id == find_item_id or item.has(find_item_id):
                return True
        return False
