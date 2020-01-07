import textwrap
from data import room_data
from parser import Parser
from room import Room
from object import Object

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
score = 0
visited_rooms = set()
suppress_room_description = False
inventory = Object.dictionary_from_id_list({"torch"})

while True:

    torch = current_room.objects.get("torch") or inventory.get("torch")
    if torch and torch.current_state == "on":
        if "lit" in current_room.states:
            current_room.current_state = "lit"

    if not current_room.id in visited_rooms:
        score += 10
        visited_rooms.add(current_room.id)

    if not suppress_room_description:
        print (current_room.full_description(WRAP_WIDTH))

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
            o = current_room.get(parser.noun) or inventory.get(parser.noun)
            if o:
                print(textwrap.fill("It is " + o.description, WRAP_WIDTH))
            else:
                print("You don't see that here")

    elif parser.verb == "go":
        next_room_id = current_room.room_id_from_exit(parser.noun)
        if next_room_id:
            current_room = rooms[next_room_id]
        else:
            print("There are no exits that way.")

    elif parser.verb == "inventory":
        suppress_room_description = True
        if inventory:
            print("You are carrying: ")
            for object in inventory.values():
                print("  " + object.name)
        else:
            print("You aren't carrying anything")
    elif parser.verb == "take":
        suppress_room_description = True
        if current_room.has(parser.noun):
            taken = current_room.take(parser.noun)
            if taken:
                inventory[parser.noun] = taken
                print("You have taken " + inventory[parser.noun].name)
            else:
                print("You don't seem to be able to do that.")
        else:
            print("There isn't one of those here.")
    elif parser.verb == "drop":
        suppress_room_description = True
        if parser.noun in inventory:
            object = inventory.pop(parser.noun)
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
        print("You have scored " + str(score) + " points.")
    elif parser.verb == "quit":
        print("Thank you for playing. Your score was " + str(score))
        break
