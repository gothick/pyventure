from traits import ClothesHorse, IVerbable
from room import Room
from enum import Enum, auto
from words import Verb, Noun

class BeardHealth(Enum):
    STRAGGLY_MESS = auto()
    QUITE_TIDY = auto()
    PERFECTION = auto()


class Player(ClothesHorse, IVerbable):
    def __init__(self, inventory, wearing, score, health, caffeine_level):
        super().__init__(inventory, wearing)
        self.score = score
        self.health = health
        self.beard_status = BeardHealth.STRAGGLY_MESS
        self.caffeine_level = caffeine_level # milligrams
    
    def award_points(self, points):
        self.score += points

    def can_verb(self, verb):
        if verb == Verb.COMB:
            if self.has(Noun.COMB):
                return (True, None)
            else:
                return (False, "You'll need to find a comb first.")
        return(False, "You just can't do that to yourself.")

    def do_verb(self, verb):
        if verb == Verb.COMB:
            if self.has(Noun.COMB):
                if self.beard_status == BeardHealth.PERFECTION:
                    return (True, "You're beautiful enough already.")
                elif self.beard_status == BeardHealth.QUITE_TIDY:
                    if self.is_wearing(Noun.BEARD_OIL):
                        self.beard_status = BeardHealth.PERFECTION
                        return (True, "You shape your beard to perfection, and carefully curl the ends of your moustache. You look like your normal self again.")
                    else:
                        return (False, "You probably need to find some beard oil before you can make yourself look human again.")
                elif self.beard_status == BeardHealth.STRAGGLY_MESS:
                    if self.is_wearing(Noun.BEARD_OIL):
                        self.beard_status = BeardHealth.PERFECTION
                        return (True, "You shape your beard to perfection, and carefully curl the ends of your moustache. You look like your normal self again.")
                    else:
                        self.beard_status = BeardHealth.QUITE_TIDY
                        return (True, "Your beard isn't quite such a shocking mess now, but you clearly need to find some beard oil to restore it to its full glory.")                    
            else:
                return (False, "You need to find a comb before you do that, and maybe some beard oil for good measure.")
        return (False, "You just can't do that to yourself.")

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
    def can_touch(self, item_id, current_room: Room):
        if current_room.has(item_id) or self.has(item_id):
            return True
        return False

    @property
    def is_dead(self):
        if self.health <= 0:
            return True
        return False

    @property
    def description(self):
        pass


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