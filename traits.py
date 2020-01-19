from abc import ABC, abstractmethod
from typing import Hashable, Optional
# I know interfaces aren't terribly Pythony, but I'm experimenting with
# having containers (as in things in the game that can hold stuff, not
# the Container pattern!) implemented by a mixin here and also by 
# composition in StatefulContanerItem, and it helps to know that the
# interfaces are consistent, so they both conform to IContainer.
class IContainer(ABC):
    @abstractmethod
    def give(self, item):
        pass

    @abstractmethod
    def is_carrying_anything(self, item):
        pass
    
    @abstractmethod
    def has(self, item_id):
        pass

    @abstractmethod
    def take(self, item_id):
        pass

    @abstractmethod
    def get_item_reference(self, item_id):
        pass

class IVerbable(ABC):
    @abstractmethod
    def can_verb(self, verb: Hashable) -> (bool, Optional[str]):
        pass
    
    def do_verb(self, verb: Hashable) -> (bool, Optional[str]):
        pass

class IVerbNounable(IVerbable):
    def can_verb(self, verb: Hashable, noun: Hashable = None) -> (bool, Optional[str]):
        pass
    
    def do_verb(self, verb: Hashable, noun: Hashable = None) -> (bool, Optional[str]):
        pass


class Container(IContainer):
    def __init__(self, inventory, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inventory = inventory

    def give(self, item):
        self.inventory[item.id] = item

    def is_carrying_anything(self):
        return len(self.inventory) > 0
    
    def has(self, item_id):
        if item_id in self.inventory:
            return True
        for item in self.inventory.values():
            if isinstance(item, IContainer):
                if item.has(item_id):
                    return True
        return False
    
    def take(self, item_id):
        if item_id in self.inventory:
            if self.inventory[item_id].has_trait("moveable"):
                return (self.inventory.pop(item_id), None)
            else:
                return (None, "You don't seem to be able to do that.")
        for item in self.inventory.values():
            if isinstance(item, IContainer):
                (found_item, message) = item.take(item_id)
                if found_item:
                    return (found_item, message)
        return (None, "You aren't carrying that.")

    # Basically "take" only we pass our client a 
    # reference to the item that they should only
    # use temporariliy. We still hold the item.
    def get_item_reference(self, item_id):
        if item_id in self.inventory:
            return self.inventory[item_id]
        for item in self.inventory.values():
            if isinstance(item, IContainer):
                found_item = item.get_item_reference(item_id)
                if found_item:
                    return found_item
        return None

    
    def __repr__(self):
        if self.inventory:
            return "Container with items: " + ", ".join(item.name for item in self.inventory)
        return "(Empty Container)"
    
class ClothesHorse(Container):
    def __init__(self, inventory, wearing):
        super().__init__(inventory)
        self.wearing = wearing
    
    def has(self, item_id):
        return super().has(item_id) or item_id in self.wearing

    def is_carrying_anything(self):
        return super().is_carrying_anything or len(self.wearing > 0)

    def is_wearing(self, item_id):
        return item_id in self.wearing
    
    # Basically "take" only we pass our client a 
    # reference to the item that they should only
    # use temporariliy. We still hold the item.
    def get_item_reference(self, item_id):
        return super().get_item_reference(item_id) or self.wearing.get(item_id)

    def take(self, item_id):
        if item_id in self.wearing:
            if self.wearing[item_id].has_trait("moveable"):
                return (self.wearing.pop(item_id), None)
            else:
                return (None, "You don't want to take that off.")
        return super().take(item_id)
    
    def wear(self, item_id):
        if self.is_wearing(item_id):
            return (False, "You're already wearing that.")
        if item_id in self.inventory:
            if self.inventory[item_id].has_trait("wearable"):
                trait = self.inventory[item_id].get_trait("wearable")
                (item, message) = self.take(item_id)
                if item:
                    self.wearing[item_id] = item
                    return (True, trait.get("wear_description") or f"You are now wearing {item.name}.")
                else:
                    return (False, message)
            else:
                return (False, "You can't wear that.")
        else:
            return (False, "You're not carrying that.")
        
    def unwear(self, item_id):
        if not item_id in self.wearing:
            return (False, "You're not wearing that.")
        else:
            if self.wearing[item_id].has_trait("wearable"):
                trait = self.wearing[item_id].get_trait("wearable")
                if not trait.get("unremoveable") or False:
                    item = self.wearing.pop(item_id)
                    # It goes back into our general inventory
                    self.give(item)
                    return (True, "You take off " + item.name + ".")
                else:
                    message = trait.get("unwear_description") or "You can't take that off."
                    return (False, message)
            else:
                return(False, "That doesn't seem appropriate.")

    def __repr__(self):
        debug = super().__repr__() + "\n"
        if self.wearing:
            debug += "Clothes horse wearing: " + ", ".join(self.wearing)
        else:
            debug += "(Wearing nothing)"
        return debug
