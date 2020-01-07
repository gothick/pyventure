from object import Object

class Player:
    def __init__(self, inventory, wearing, score, health, caffeine_level):
        self.score = score
        self.health = health
        self.caffeine_level = caffeine_level # milligrams
        # Dictionary of object IDs to actual objects
        self.inventory = inventory
        self.wearing = wearing
    
    def give(self, object):
        self.inventory[object.id] = object
    
    def award_points(self, points):
        self.score += points

    @property
    def is_carrying_anything(self):
        return len(self.inventory) > 0 or len(self.wearing) > 0
    
    def is_carrying(self, object_id):
        return object_id in self.inventory or object_id in self.wearing

    def is_wearing(self, object_id):
        return object_id in self.wearing

    def take(self, object_id):
        if object_id in self.inventory:
            return self.inventory.pop(object_id)
        elif object_id in self.wearing:
            return self.wearing.pop(object_id)
        return None

    def wear(self, object_id):
        if object_id in self.wearing:
            return "You're already wearing that."
        if object_id in self.inventory:
            if self.inventory[object_id].wearable == True:
                object = self.inventory.pop(object_id)
                self.wearing[object_id] = object
                return "You are now wearing " + object.name
            else: 
                return "You can't wear that."
        return "You're not carrying that."

    def unwear(self, object_id):
        if not object_id in self.wearing:
            return "You're not wearing that."
        else:
            object = self.wearing.pop(object_id)
            self.inventory[object_id] = object
            return "You take off " + object.name

    def __repr__(self):
        message = f"A Player object with health {self.health}, caffeine_level {self.caffeine_level} and score {self.score}\n"
        message += "Carrying:\n"
        for object in self.inventory:
            message += f" {object}\n"
        message += "Wearing:\n"
        for object in self.wearing:
            message += f" {object}\n"
        return message
        
    @property
    def is_dead(self):
        if self.health <= 0:
            return True
        return False

    def tick(self):
        messages = []
        self.caffeine_level -= 1 
        if self.caffeine_level >= 50:
            # We're fine and dandy.
            pass
        elif self.caffeine_level == 49:
            messages.append("You feel tired and hung-over, and lacking in coffee.")
        elif self.caffeine_level == 39:
            messages.append("You could really do with a cup of coffee.")
        elif self.caffeine_level == 29:
            messages.append("Seriously, dude. This headache might just kill you if you don't get a coffee soon.")
        elif self.caffeine_level == 19:
            messages.append("You let out an involuntary moan and clutch your forehead. Going cold turkey on cortados is really harshing your mellow.")
        elif self.caffeine_level < 19 and self.caffeine_level > 0:
            messages.append("Your coffee levels are critical. You must find a café immediately.")
        elif self.caffeine_level <= 0:
            self.health = 0
            messages.append("You caffeine levels have fallen below a critical threshold. The world spins as you crumple to the floor.")
        return messages