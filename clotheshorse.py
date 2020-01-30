from container import Container
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
        item_to_wear = self.inventory.get(item_id)
        if item_to_wear:
            # Note that a trait can be an empty dictionary, so has_trait is a better check for existence
            # than getting the trait and checking it (as an empty dictionary evaluates to False)
            if item_to_wear.has_trait("wearable"):
                wearable_trait = item_to_wear.get_trait("wearable")
                slot_name = wearable_trait.get("slot")
                if slot_name and self.wearing_in_slot(slot_name):
                   return (False, "You'll need to take something off first.")
                (item, message) = self.take(item_id)
                self.wearing[item_id] = item
                return (True, wearable_trait.get("wear_description") or f"You are now wearing {item.name}.")
            else:
                return (False, "You can't wear that.")
        else:
            return (False, "You're not carrying that.")

    def wearing_in_slot(self, slot_name):
        # Simple code for now as we never allow the player to wear 
        # more than one item per slot.
        for item in self.wearing.values():
            if item.get_trait("wearable").get("slot") == slot_name:
                return item
        return None

    @property
    def is_fully_clothed(self):
        return self.wearing_in_slot("top") is not None and self.wearing_in_slot("bottom") is not None
        
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
