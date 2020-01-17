import textwrap
import data
from parser import Parser
from room import Room
from player import Player
from item import ItemFactory
from words import Noun, Verb, DIRECTIONS, normalised_nouns, normalised_verbs
from textwrap import TextWrapper

# All our printed output goes through here.
class Outputter:
    def __init__(self, wrap_width = 80):
        self.wrapper = TextWrapper(width = wrap_width)
    def print(self, text = ""):
        # "If replace_whitespace is false, newlines may appear in the middle of a
        #  line and cause strange output. For this reason, text should be split 
        #  into paragraphs (using str.splitlines() or similar) which are wrapped
        #  separately." -- https://docs.python.org/3/library/textwrap.html
        # "Sigh" -- me
        for line in text.splitlines():
            print(self.wrapper.fill(line))

o = Outputter()

# All our items are stamped out from this data-driven
# item factory.
item_factory = ItemFactory(data.item_data)

rooms = {}

# Build the universe.
for id, data in data.room_data.items():
    rooms[id] = Room(id, item_factory, data)

o.print("\nWelcome to the Bristol Hipster Adventure.\n")

current_room = rooms["livingroom"]
visited_rooms = set()
suppress_room_description = False

player = Player(
    inventory = {},
    wearing = item_factory.create_dictionary_from_nouns([Noun.SHIRT, Noun.BOXER_SHORTS]),
    score = 0,
    health = 100, # percent
    caffeine_level = 50 # milligrams
)

debugging = False 

parser = Parser(Noun, Noun.UNKNOWN, Verb, Verb.GO, DIRECTIONS, normalised_nouns, normalised_verbs)

while True:

    torch = current_room.get_item_reference("torch") or player.get_item_reference("torch")
    if torch and torch.current_state == "on":
        if "lit" in current_room.states:
            current_room.current_state = "lit"

    if not current_room.id in visited_rooms:
        player.award_points(10)
        visited_rooms.add(current_room.id)

    if not suppress_room_description:
        o.print()
        o.print(current_room.full_description)

    # Pre-round player events:
    player_messages = player.tick()
    for message in player_messages:
        o.print(message)

    # print(player)

    if player.is_dead:
        o.print(f"You have died. Your final score was {player.score} points.")
        break

    suppress_room_description = False

    command = input("Command: ")
    parser.parse(command)

    if debugging:
        o.print(parser.__repr__())

    if not parser.valid:
        suppress_room_description = True
        o.print("Sorry, I don't understand '" + command + "'")
        continue

    if parser.verb == Verb.EXAMINE:
        if not parser.noun:
            o.print("You look around.")
        else:
            suppress_room_description = True
            item = current_room.get_item_reference(parser.noun) or player.inventory.get(parser.noun) or player.wearing.get(parser.noun)
            if item:
                o.print("It is " + item.description)
            else:
                o.print("You don't see that here")

    elif parser.verb == Verb.GO:
        (can_go, objection) = current_room.can_go(parser.noun, player)
        if can_go:
            next_room_id = current_room.room_id_from_exit(parser.noun)
            transition = current_room.transition_from_exit(parser.noun)
            if transition:
                o.print()
                o.print(transition)
            current_room = rooms[next_room_id]
        else:
            suppress_room_description = True
            o.print(objection)

    elif parser.verb == Verb.INVENTORY:
        suppress_room_description = True
        if player.is_carrying_anything:
            o.print("You are carrying: ")
            if player.inventory:
                for object in player.inventory.values():
                    o.print(f"  {object.name}")
            if len(player.wearing) > 0:
                for object in player.wearing.values():
                    o.print(f"  {object.name} (worn)")

        else:
            o.print("You aren't carrying anything")
    elif parser.verb == Verb.TAKE:
        suppress_room_description = True
        if player.has(parser.noun):
            o.print("You already have that.")
        else:
            if current_room.has(parser.noun):
                (taken, message) = current_room.take(parser.noun)
                if taken:
                    player.give(taken)
                    o.print("You have taken " + taken.name)
                else:
                    o.print(message)
            else:
                o.print("There isn't one of those here.")
    elif parser.verb == Verb.DROP:
        suppress_room_description = True
        item = player.get_item_reference(parser.noun)
        if item:
            if item.has_trait("moveable"):
                (item, message) = player.take(parser.noun)
                if item:
                    o.print("You drop " + item.name)
                    current_room.give(item)
                else:
                    o.print(message)
            else:
                o.print ("You don't seem to be able to do that.")
        else:
            o.print("You're not carrying one of those.")
    elif parser.verb == Verb.PUT_ON:
        suppress_room_description = True
        (result, message) = player.wear(parser.noun)
        o.print(message)
    elif parser.verb == Verb.TAKE_OFF:
        suppress_room_description = True
        (result, message) = player.unwear(parser.noun)
        o.print(message)
    elif parser.verb in [ Verb.OPEN, Verb.CLOSE ]:
        suppress_room_description = True
        item = current_room.get_item_reference(parser.noun) or player.get_item_reference(parser.noun) 
        if item:
            (result, message) = item.do_verb(parser.verb)
            # For now it doesn't matter if it was successful or not; do_verb will
            # hand us an appropriate message.
            o.print(message)
        else:
            o.print("You don't see that here")

    elif parser.verb in [ Verb.TURN_ON, Verb.TURN_OFF ]:
        suppress_room_description = True
        if player.has(parser.noun):
            item = player.get_item_reference(parser.noun)
            (result, message) = item.do_verb(parser.verb)
            # For now it doesn't matter if it was successful or not; do_verb will
            # hand us an appropriate message.
            o.print(message)
        else:
            # The thing we're turning on or off wasn't in the inventory, but
            # if it's an immovable object that's in the room with us, we still
            # want to respond.
            if current_room.has(parser.noun):
                item = current_room.get_item_reference(parser.noun)
                if item.has_trait("moveable"):
                    o.print("You'll need to pick that up first")
                else:
                    o.print("I don't know how to do that.")
            else:
                o.print("You don't see that here.")
    elif parser.verb == Verb.SCORE:
        suppress_room_description = True
        o.print(f"You have scored {player.score} points.")
    elif parser.verb == Verb.HEALTH:
        suppress_room_description = True
        o.print(f"Current health: {player.health}%")
    elif parser.verb == Verb.QUIT:
        o.print(f"Thank you for playing. Your final score was {player.score} points.")
        break
    elif parser.verb == Verb.XYZZY:
        # Deep magic
        if debugging:
            o.print("Toggling debugging OFF")
            debugging = False
        else:
            o.print("Toggling debugging ON")
            debugging = True
        o.print()
        o.print("##### Magical Debugging Start #####")
        o.print(current_room.__repr__())
        o.print(player.__repr__())
        o.print("#####  Magical Debugging End  #####")
        o.print()
        suppress_room_description = True
    else:
        o.print("Sorry, I don't understand.")

