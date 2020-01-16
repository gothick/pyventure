from traits import Container, IContainer

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
        return cls(id, item_data, self)        

    # Create a dictionary of Items from an ID list
    def create_from_id_list(self, ids):
        objects = {}
        for id in ids:
            objects[id] =  self.create_from_id(id)
        return objects

# The actual Item classes
class Item:
    def __init__(self, id, data, item_factory, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

class ContainerItem(Container, Item):
    def __init__(self, id, data, item_factory, *args, **kwargs):
        inventory = item_factory.create_from_id_list(data["inventory"])
        super().__init__(inventory, id, data, item_factory)

    @property
    def description(self):
        desc = super().description
        if self.inventory:
            desc += " It currently holds " + ", ".join(item.name for item in self.inventory.values()) + "."
        return desc

class StatefulContainerItem(StatefulItem, IContainer):
    def __init__(self, id, data, item_factory, *args, **kwargs):
        super().__init__(id, data, item_factory)
        self.inventories = {}
        for state in self.states:
            inventory = item_factory.create_from_id_list(data["inventory"][state])
            self.inventories[state] = Container(inventory)
    
    # IContainer implementation (we could have inherited from Container to get 
    # an IContainer implementation, but the fact that our inventory changes 
    # depending on what state we're in makes that complicated.
    # Here I'm composing multiple Container instances (one per state) to do the
    # work instead.
    def give(self, item):
        return self.inventories[self.state].give(item)
    
    def is_carrying_anything(self):
        return self.inventories[self.state].is_carrying_anything()
    
    def has(self, item_id):
        return self.inventories[self.state].has(item_id)

    def take(self, item_id):
        return self.inventories[self.state].take(item_id)

    def get_item_reference(self, item_id):
        return self.inventories[self.state].get_item_reference(item_id)

    # Item overrides
    @property
    def description(self):
        desc = super().description
        if self.inventories[self.state].is_carrying_anything():
            container = self.inventories[self.state]
            desc += " It currently holds " + ", ".join(item.name for item in container.inventory.values()) + "."
        return desc