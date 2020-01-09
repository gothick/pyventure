class Container:
    def __init__(self, inventory):
        self.inventory = inventory

    def give(self, item):
        self.inventory[item.id] = item

    def is_carrying_anything(self):
        return len(self.inventory) > 0
    
    def has(self, item_id):
        return item_id in self.inventory
    
    def take(self, item_id):
        if item_id in self.inventory:
            return self.inventory.pop(item_id)
        return None

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
