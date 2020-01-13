class Container:
    def __init__(self, inventory, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inventory = inventory

    def give(self, item):
        self.inventory[item.id] = item

    def is_carrying_anything(self):
        return len(self.inventory) > 0
    
    def has(self, find_item_id):
        for (item_id, item) in self.inventory.items():
            if item_id == find_item_id or item.has(find_item_id):
                return True
        return False
    
    def take(self, item_id):
        if item_id in self.inventory:
            if self.inventory[item_id].has_trait("moveable"):
                return self.inventory.pop(item_id)
        return None

    # Basically "take" only we pass our client a 
    # reference to the item that they should only
    # use temporariliy. We still hold the item.
    def get_item_reference(self, item_id):
        return self.inventory.get(item_id)
    
    def __repr__(self):
        if self.inventory:
            return "Container with items: " + ", ".join(self.inventory)
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
            return self.wearing.pop(item_id)
        return super().take(item_id)
    
    def wear(self, item_id):
        if self.wearing(item_id):
            return (False, "You're already wearing that.")
        if item_id in self.inventory:
            if self.inventory[item_id].has_trait("wearable"):
                item = self.take(item_id)
                self.wearing[item_id] = item
                return (True, "You are now wearing " + item.name + ".")
            else:
                return (False, "You can't wear that.")
        else:
            return (False, "You're not carrying that.")
        
    def unwear(self, item_id):
        if not item_id in self.wearing:
            return (False, "You're not wearing that.")
        else:
            item = self.wearing.pop(item_id)
            self.give(item)
            return (True, "You take off " + item.name + ".")

    def __repr__(self):
        debug = super().__repr__() + "\n"
        if self.wearing:
            debug += "Clothes horse wearing: " + ", ".join(self.wearing)
        else:
            debug += "(Wearning nothing)"
        return debug
