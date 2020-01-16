import textwrap
import data
from parser import Parser
from room import Room
from player import Player
from item import ItemFactory
from words import Noun, Verb, DIRECTIONS, normalised_nouns, normalised_verbs

# All our items are stamped out from this data-driven
# item factory.
item_factory = ItemFactory(data.item_data)

rooms = {}

# Build the universe.
for id, data in data.room_data.items():
    rooms[id] = Room(id, item_factory, data)

print("\nWelcome to the Bristol Hipster Adventure.\n")

WRAP_WIDTH = 80

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
        print()
        print (current_room.full_description(WRAP_WIDTH))

    # Pre-round player events:
    player_messages = player.tick()
    for message in player_messages:
        print(textwrap.fill(message, WRAP_WIDTH))

    # print(player)

    if player.is_dead:
        print(f"You have died. Your final score was {player.score} points.")
        break

    suppress_room_description = False

    command = input("Command: ")
    parser.parse(command)

    if debugging:
        print(parser)

    if not parser.valid:
        suppress_room_description = True
        print("Sorry, I don't understand '" + command + "'")
        continue

    if parser.verb == Verb.EXAMINE:
        if not parser.noun:
            print("You look around.")
        else:
            suppress_room_description = True
            o = current_room.get_item_reference(parser.noun) or player.inventory.get(parser.noun) or player.wearing.get(parser.noun)
            if o:
                print(textwrap.fill("It is " + o.description, WRAP_WIDTH))
            else:
                print("You don't see that here")

    elif parser.verb == Verb.GO:
        (can_go, objection) = current_room.can_go(parser.noun, player)
        if can_go:
            next_room_id = current_room.room_id_from_exit(parser.noun)
            transition = current_room.transition_from_exit(parser.noun)
            if transition:
                print()
                print(textwrap.fill(transition, WRAP_WIDTH))
            current_room = rooms[next_room_id]
        else:
            suppress_room_description = True
            print(objection)

    elif parser.verb == Verb.INVENTORY:
        suppress_room_description = True
        if player.is_carrying_anything:
            print("You are carrying: ")
            if player.inventory:
                for object in player.inventory.values():
                    print(f"  {object.name}")
            if len(player.wearing) > 0:
                for object in player.wearing.values():
                    print(f"  {object.name} (worn)")

        else:
            print("You aren't carrying anything")
    elif parser.verb == Verb.TAKE:
        suppress_room_description = True
        if player.has(parser.noun):
            print("You already have that.")
        else:
            if current_room.has(parser.noun):
                (taken, message) = current_room.take(parser.noun)
                if taken:
                    player.give(taken)
                    print("You have taken " + taken.name)
                else:
                    print(message)
            else:
                print("There isn't one of those here.")
    elif parser.verb == Verb.DROP:
        suppress_room_description = True
        item = player.get_item_reference(parser.noun)
        if item:
            if item.has_trait("moveable"):
                (item, message) = player.take(parser.noun)
                if item:
                    print("You drop " + item.name)
                    current_room.give(item)
                else:
                    print(message)
            else:
                print ("You don't seem to be able to do that.")
        else:
            print("You're not carrying one of those.")
    elif parser.verb == Verb.PUT_ON:
        suppress_room_description = True
        (result, message) = player.wear(parser.noun)
        print(textwrap.fill(message,  WRAP_WIDTH))
    elif parser.verb == Verb.TAKE_OFF:
        suppress_room_description = True
        (result, message) = player.unwear(parser.noun)
        print(textwrap.fill(message,  WRAP_WIDTH))
    elif parser.verb in [ Verb.OPEN, Verb.CLOSE ]:
        suppress_room_description = True
        item = current_room.get_item_reference(parser.noun) or player.get_item_reference(parser.noun) 
        if item:
            (result, message) = item.do_verb(parser.verb)
            # For now it doesn't matter if it was successful or not; do_verb will
            # hand us an appropriate message.
            print(textwrap.fill(message))
        else:
            print("You don't see that here")

    elif parser.verb in [ Verb.TURN_ON, Verb.TURN_OFF ]:
        suppress_room_description = True
        if player.has(parser.noun):
            item = player.get_item_reference(parser.noun)
            (result, message) = item.do_verb(parser.verb)
            # For now it doesn't matter if it was successful or not; do_verb will
            # hand us an appropriate message.
            print(textwrap.fill(message))
        else:
            # The thing we're turning on or off wasn't in the inventory, but
            # if it's an immovable object that's in the room with us, we still
            # want to respond.
            if current_room.has(parser.noun):
                item = current_room.get_item_reference(parser.noun)
                if item.has_trait("moveable"):
                    print("You'll need to pick that up first")
                else:
                    print("I don't know how to do that.")
            else:
                print("You don't see that here.")
    elif parser.verb == Verb.SCORE:
        suppress_room_description = True
        print(f"You have scored {player.score} points.")
    elif parser.verb == Verb.HEALTH:
        suppress_room_description = True
        print(f"Current health: {player.health}%")
    elif parser.verb == Verb.QUIT:
        print(f"Thank you for playing. Your final score was {player.score} points.")
        break
    elif parser.verb == Verb.XYZZY:
        # Deep magic
        if debugging:
            print("Toggling debugging OFF")
            debugging = False
        else:
            print("Toggling debugging ON")
            debugging = True
        print()
        print("##### Magical Debugging Start #####")
        print(current_room)
        print(player)
        print("#####  Magical Debugging End  #####")
        print()
        suppress_room_description = True

