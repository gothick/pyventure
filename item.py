from container import Container, IContainer
from verbable import IVerbable
from utility import commalist
import random

# Very simple Item factory.
class ItemFactory:
    # Create a factory given a dictionary of item data:
    def __init__(self, data):
        self.data = data

    def create_from_noun(self, noun):
        if noun not in self.data:
            raise Exception(f"Could not find item with id '{noun}' in item data")
        item_data = self.data[noun]
        type = item_data.get("type") or "Item" # Default to the simplest item type
        cls = globals()[type]
        return cls(noun, item_data, self)        

    def create_dictionary_from_nouns(self, nouns):
        items = {}
        for noun in nouns:
            items[noun] =  self.create_from_noun(noun)
        return items

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
    
    def get_trait(self, trait):
        return self.traits.get(trait)

def __repr__(self):
    return f"{self.name}: {self.description}"

class SimpleVerbableItem(Item, IVerbable):
    def __init__(self, id, data, item_factory, *args, **kwargs):
        super().__init__(id, data, item_factory, *args, **kwargs)
        self.verbs = data.get("verbs") or set()

    def do_verb(self, verb_id, environment_rules = {}, extras = {}):
        result = (False, "You can't do that.")
        verb = self.verbs.get(verb_id)
        if verb:
            if verb["type"] == "random":
                message = random.choice(verb["messages"])
            else:
                message = verb["message"]
            result = (True, message)
        return result

class StatefulItem(Item, IVerbable):
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

    def apply_rules(self, verb_rules, environment_rules = {}, extras = {}):
        for rule in verb_rules:
            if rule["type"] == "current_state":
                if self.state not in rule["states"]:
                    return (False, rule["message"])
            elif rule["type"] == "not_below_appearance_level":
                if "player_appearance_level" not in extras:
                    raise Exception("Appearance rule running but no appearance extra passed in.")
                if extras["player_appearance_level"] < rule["level"]:
                    return (False, rule["message"])
        return (True, None)


    def do_verb(self, verb_id, environment_rules = {}, extras = {}):
        result = (False, "You can't do that.")
        verb = self.verbs.get(verb_id)
        if verb:
            # Sanity check
            requires_extras = verb.get("requires_extras") or set()
            if not all(extra in extras.keys() for extra in requires_extras):
                raise Exception(f"Item '{self.id}' doing verb '{verb_id}' requires missing extra. Found extras {extras.keys()}; requires extras {requires_extras}")

            verb_rules = verb.get("rules") or []
            (rules_result, message) = self.apply_rules(verb_rules, environment_rules, extras)

            if rules_result == True: 
                if "new_state" in verb:
                    if self.state != verb["new_state"]:
                        self.state = verb["new_state"]
                        result = (True, verb["message"])
                    else:
                        result = (False, "Nothing happens.")
                else:
                    # Sometimes we just have specific failure messages for comic effect.
                    result = (False, verb["message"])
            else:
                result = (rules_result, message)
        return result

class ContainerItem(Container, Item):
    def __init__(self, id, data, item_factory, *args, **kwargs):
        inventory = item_factory.create_dictionary_from_nouns(data["inventory"])
        super().__init__(inventory, id, data, item_factory)

    @property
    def description(self):
        desc = super().description
        if self.inventory:
            desc += " It currently holds " + commalist(list(item.name for item in self.inventory.values())) + "."
        return desc

class StatefulContainerItem(StatefulItem, IContainer):
    def __init__(self, id, data, item_factory, *args, **kwargs):
        super().__init__(id, data, item_factory)
        self.inventories = {}
        for state in self.states:
            inventory = item_factory.create_dictionary_from_nouns(data["inventory"][state])
            self.inventories[state] = Container(inventory)
    
    # IContainer implementation 
    # We could have inherited from Container to get an IContainer implementation, 
    # but the fact that our inventory changes depending on what state we're in 
    # makes that complicated. Here I'm composing multiple Container instances 
    # (one per state) to do the work instead.
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
            desc += " It currently holds " + commalist(list(item.name for item in container.inventory.values())) + "."
        return desc