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
    