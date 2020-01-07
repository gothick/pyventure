from object import Object

class Player:
    def __init__(self, object_ids, score, health, caffeine_level):
        self.score = score
        self.health = health
        self.caffeine_level = caffeine_level # milligrams
        # Dictionary of object IDs to actual objects
        self.inventory = Object.dictionary_from_id_list(object_ids)
    def give(self, object):
        self.inventory[object.id] = object
    
    def award_points(self, points):
        self.score += points

    @property
    def is_carrying_anything(self):
        return len(self.inventory) > 0
    
    def is_carrying(self, object_id):
        return object_id in self.inventory

    def take(self, object_id):
        if object_id in self.inventory:
            return self.inventory.pop(object_id)
        return None

    def __repr__(self):
        return f"A Player object with health {self.health}, caffeine_level {self.caffeine_level} and score {self.score}"
        
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