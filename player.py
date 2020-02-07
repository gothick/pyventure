from verbable import IVerbable
from clotheshorse import ClothesHorse
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
        self.riding = None
        self.health = health
        self.beard_status = BeardHealth.STRAGGLY_MESS
        self.caffeine_level = caffeine_level # milligrams
    
    def mirror_description(self, reflective_item_description):
        description = f"{reflective_item_description}, you "
        if self.beard_status == BeardHealth.STRAGGLY_MESS:
            description += "look like a wildman, with an unkempt beard. "
            if self.is_wearing(Noun.BEARD_OIL):
                description += "The beard is covered in oil, but you need to use a comb. "
        elif self.beard_status == BeardHealth.QUITE_TIDY:
            description += "look vaguely human, though your beard could use a bit more maintenance. "
        else:
            description += "admire your perfectly-combed beard and glossy moustache. "
        
        if self.caffeine_level < 50:
            description += "You look like you could use a coffee."
        elif self.caffeine_level < 20:
            desciption += "You look pale and drawn, though, and desperately in need of a cortado."
        return description

    def award_points(self, points):
        self.score += points

    @property
    def is_riding_anything(self):
        return not self.riding is None

    @property
    def appearance_level(self):
        return 100 if self.beard_status == BeardHealth.PERFECTION else 0

    def is_riding(self, noun):
        return not self.riding is None and self.riding.id == noun
    
    def take(self, item_id):
        if self.riding and self.riding.id == item_id:
            return (None, "You'll need to dismount that first.")
        return super().take(item_id)

    def do_verb(self, verb, noun = None, environment_rules = {}, extras = {}):
        if verb == Verb.COMB:
            return self.do_comb(verb, noun)
        elif verb == Verb.RIDE:
            return self.do_ride(verb, noun, environment_rules)
        elif verb == Verb.DISMOUNT:
            return self.do_dismount(verb, noun, environment_rules)
        return (False, "You just can't do that to yourself.")

    def do_comb(self, verb, noun = None):
        if noun is None:
            return (False, "Comb what?")
        if noun != Noun.BEARD:
            return (False, "You can't comb that.")
        if not self.has(Noun.COMB):
            if not self.has(Noun.BEARD_OIL):
                return (False, "You need to find a comb before you do that, and maybe some beard oil for good measure.")
            else:
                return (False, "You need to find a comb before you do that.")
        if self.beard_status == BeardHealth.PERFECTION:
            return (True, "You're beautiful enough already.")

        if self.beard_status == BeardHealth.QUITE_TIDY:
            if self.is_wearing(Noun.BEARD_OIL):
                self.beard_status = BeardHealth.PERFECTION
                return (True, "You shape your beard to perfection, and carefully curl the ends of your moustache. You look like your normal self again.")
            else:
                if self.has(Noun.BEARD_OIL):
                    return (False, "You probably want to apply the beard oil first.")
                else:
                    return (False, "You probably need to find some beard oil before you can make yourself look human again.")

        else: # Must be STRAGGLY_MESS
            if self.is_wearing(Noun.BEARD_OIL):
                self.beard_status = BeardHealth.PERFECTION
                return (True, "You shape your beard to perfection, and carefully curl the ends of your moustache. You start to feel like your normal self again.")
            else:
                self.beard_status = BeardHealth.QUITE_TIDY
                return (True, "Your beard isn't quite such a shocking mess now, but you clearly need to find some beard oil to restore it to its full glory.")                    

    def do_ride(self, verb, noun = None, environment_rules = {}):
        if not self.riding:
            item = self.get_item_reference(noun)
            if item:
                if item.has_trait("rideable"):
                    rule = environment_rules.get("can_ride")
                    if rule:
                        return rule
                    else:
                        self.riding = self.get_item_reference(Noun.PENNY_FARTHING)
                        return (True, f"You're now proudly riding {self.riding.name}.")
                else:
                    return (False, "You can't ride that.")
            else:
                return (False, "You'll have to get that to try riding it.")    
        else:
            return (False, f"You're already riding {self.riding.name}")

    def do_dismount(self, verb, noun = None, environment_rules = {}):
        if self.riding:
            if self.riding.id == noun:
                self.riding = None
                return (True, "You dismount neatly.")
            else:
                return (False, "You're not riding that.")
        else:
            return (False, "You're not riding anything.")

    def __repr__(self):
        message = f"A Player object with health {self.health}, caffeine_level {self.caffeine_level} and score {self.score}\n"
        message += "Carrying:\n"
        for object in self.inventory:
            message += f" {object}\n"
        message += "Wearing:\n"
        for object in self.wearing:
            message += f" {object}\n"
        if self.riding:
            message += f"Riding: {self.riding.name}\n"
        else:
            message += "Riding nothing\n"
        return message
    
    # TODO Should this be a Room, or just a Container interface I pass as 
    # something like container_environment? Might make things more loosely
    # coupled if I don't refer to rooms in here.
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

        withdrawal_messages = [
            { "min": 49, "max": 49, "message": "You feel tired and hung-over, and lacking in coffee."},
            { "min": 39, "max": 39, "message": "You could really do with a cup of coffee."},
            { "min": 29, "max": 29, "message": "Seriously, dude. This headache might just kill you if you don't get a coffee soon."},
            { "min": 19, "max": 19, "message": "You let out an involuntary moan and clutch your forehead. Going cold turkey on cortados is really harshing your mellow."},
            { "min": 1,  "max": 18, "message": "Your coffee levels are critical. You must find a café immediately."},
            { "min": 0,  "max": 0, "new_health": 0, "message": "Your caffeine levels have fallen below a critical threshold. The world spins as you crumple to the floor."}
        ]

        messages = []
        self.caffeine_level -= 1 
        for withdrawal_message in withdrawal_messages:
            if self.caffeine_level >= withdrawal_message["min"] and self.caffeine_level <= withdrawal_message["max"]:
                messages.append(withdrawal_message["message"])
                new_health = withdrawal_message.get("new_health")
                if not new_health is None:
                    self.health = new_health

        return messages