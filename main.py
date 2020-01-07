import textwrap
from data import room_data
from parser import Parser
from room import Room
from object import Object
from player import Player

rooms = {}

# Build the universe.
for room_id in room_data:

    rooms[room_id] = Room(room_id,
                       room_data[room_id]["name"],
                       room_data[room_id]["description"],
                       room_data[room_id]["objects"],
                       room_data[room_id]["exits"],
                       room_data[room_id]["states"]
    )

print("\nWelcome to the Bristol Hipster Adventure.\n")

WRAP_WIDTH = 80

current_room = rooms["livingroom"]
visited_rooms = set()
suppress_room_description = False

player = Player(
    object_ids = {"torch"},
    score = 0,
    health = 100, # percent
    caffeine_level = 50 # milligrams
)

while True:

    torch = current_room.objects.get("torch") or player.inventory.get("torch")
    if torch and torch.current_state == "on":
        if "lit" in current_room.states:
            current_room.current_state = "lit"

    if not current_room.id in visited_rooms:
        player.award_points(10)
        visited_rooms.add(current_room.id)

    if not suppress_room_description:
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
    parser = Parser(command)

    if not parser.valid:
        suppress_room_description = True
        print("Sorry, I don't understand '" + command + "'")
        continue

    if parser.verb == "examine":
        if not parser.noun:
            print("You look around.")
        else:
            suppress_room_description = True
            o = current_room.get(parser.noun) or player.inventory.get(parser.noun)
            if o:
                print(textwrap.fill("It is " + o.description, WRAP_WIDTH))
            else:
                print("You don't see that here")

    elif parser.verb == "go":
        (can_go, objection) = current_room.can_go(parser.noun, player.inventory)
        if can_go:
            next_room_id = current_room.room_id_from_exit(parser.noun)
            current_room = rooms[next_room_id]
        else:
            suppress_room_description = True
            print(objection)

    elif parser.verb == "inventory":
        suppress_room_description = True
        if player.is_carrying_anything:
            print("You are carrying: ")
            for object in player.inventory.values():
                print("  " + object.name)
        else:
            print("You aren't carrying anything")
    elif parser.verb == "take":
        suppress_room_description = True
        if current_room.has(parser.noun):
            taken = current_room.take(parser.noun)
            if taken:
                player.give(taken)
                print("You have taken " + taken.name)
            else:
                print("You don't seem to be able to do that.")
        else:
            print("There isn't one of those here.")
    elif parser.verb == "drop":
        suppress_room_description = True
        if player.is_carrying(parser.noun):
            object = player.take(parser.noun)
            print("You drop " + object.name)
            current_room.add_object(object)
        else:
            print("You're not carrying one of those.")
    elif parser.verb in [ "turn on", "turn off" ]:
        suppress_room_description = True
        if parser.noun in inventory:
            o = inventory[parser.noun]
            if o.do_verb(parser.verb):
                print("You " + parser.verb + " " + o.name)
                print(textwrap.fill("You are now holding " + o.description,  WRAP_WIDTH))
                if parser.verb == "turn on" and parser.noun == "torch":
                    if "lit" in current_room.states and current_room.current_state != "lit":
                        current_room.current_state = "lit"
                        suppress_room_description = False
                if parser.verb == "turn off" and parser.noun == "torch":
                    if "unlit" in current_room.states and current_room.current_state != "unlit":
                        current_room.current_state = "unlit"
                        suppress_room_description = False
            else:
                print("Nothing happens")
        else:
            # The thing we're turning on or off wasn't in the inventory, but
            # if it's an immovable object that's in the room with us, we still
            # want to respond.
            if current_room.has(parser.noun):
                o = current_room.get(parser.noun)
                if o.moveable:
                    print("You'll need to pick that up first")
                else:
                    if o.id == "tv":
                        print("You don't see how to do that. Is there a remote somewhere?")
                    else:
                        print("I don't know how to do that.")
            else:
                print("You don't see that here.")
    elif parser.verb == "score":
        suppress_room_description = True
        print(f"You have scored {player.score} points.")
    elif parser.verb == "health":
        suppress_room_description = True
        print(f"Current health: {player.health}%")
    elif parser.verb == "quit":
        print(f"Thank you for playing. Your final score was {player.score} points.")
        break
    elif parser.verb == "xyzzy":
        # Deep magic
        print()
        print("##### Magical Debugging Start #####")
        print(current_room)
        print(player)
        print("#####  Magical Debugging End  #####")
        print()
        suppress_room_description = True

