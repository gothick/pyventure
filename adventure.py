objects = {
    "torch": {
        "name": "an Ever Ready torch",
        "description": "a plastic 1970s Ever Ready torch"
    },
    "iphone": {
        "name": "an iPhone SE",
        "description": "an iPhone SE. It seems to be connected to the house WiFi."
    }
}

rooms = {
    "lounge": {
        "name": "lounge",
        "objects": { "iphone" },
        "description": "You are a dusty living room, full to the (peeling) ceiling with stuff.",
        "exits": {
            "north": "kitchen",
            "south": "street"
        }
    },
    "kitchen": {
        "name": "kitchen",
        "objects": set(),
        "description": "You are in a squalid kitchen. There may be work surfaces somewhere under the pile of mouldering plates and pans, but it's hard to tell.",
        "exits": {
            "south": "lounge",
            "north": "bathroom"
        }
    },
    "street": {
        "name": "street",
        "objects": set(),
        "description": "You are in a Victorian terraced street in Bristol. It is raining.",
        "exits": {
            "north": "lounge"
            }
        },
    "bathroom": {
        "name": "bathroom",
        "objects": set(),
        "description": "You are in a dark bathroom. You pull the light cord, and are rewarded with a disappointing 'clunk', and no additional light.",
        "exits": {
            "south": "kitchen"
            }
        }
    }

def carrying(object_id):
    if object_id in inventory:
        return True
    return False

def is_in_room(object_id, room):
    if object_id in room["objects"]:
        return True
    return False


def find_room(current_room, direction):
    new_room = None
    if direction in current_room["exits"]:
        new_room = rooms[current_room["exits"][direction]]
    else:
        print("There are no exits that way")
        new_room = current_room
        
    return new_room

print("Welcome to Squalid Adventure.")
current_room = rooms["lounge"]
score = 0
visited_rooms = set()
inventory = { "torch" }
suppress_room_description = False

while True:
    if not suppress_room_description:
        print(current_room["description"])

        for object_id in current_room["objects"]:
            print ("There is " + objects[object_id]["name"] + " here")

    suppress_room_description = False
    
    if current_room["name"] not in visited_rooms:
        score = score + 10
        visited_rooms.add(current_room["name"])

    command = input("Command: ").lower()
    
    if command == "look":
        print("You look around.")
    elif command == "go north" or command == "n":
        current_room = find_room(current_room, "north")
    elif command == "go south" or command == "s":
        current_room = find_room(current_room, "south")
    elif command == "score":
        suppress_room_description = True
        print("Your score is " + str(score))
    elif command == "inventory":
        suppress_room_description = True
        print("You are carrying:")
        for thing in inventory:
            print("  " + objects[thing]["name"])
    elif command.startswith("describe ") or command.startswith("examine "):
        suppress_room_description = True
        object_name = command[command.find(" ")+1:]
        if carrying(object_name) or is_in_room(object_name, current_room):
            object = objects[object_name]
            print("You look at the " + object["name"] + ". It is " + object["description"] + ".")
        else:
            print("There is no " + object_name + " here")
    elif command.startswith("take ") or command.startswith("get "):
        object_name = command[command.find(" ")+1:]
        if carrying(object_name):
            print("You are already carrying " + objects[object_name]["name"])
        elif is_in_room(object_name, current_room):
            current_room["objects"].remove(object_name)
            inventory.add(object_name)
            print("You take the " + objects[object_name]["name"])
        else:
            print("There is no " + object_name + " here")
    elif command.startswith("drop "):
        object_name = command[command.find(" ")+1:]
        if carrying(object_name):
            print("You drop " + objects[object_name]["name"])
            inventory.remove(object_name)
            current_room["objects"].add(object_name)
        else:
            print("You aren't carrying that.")
    elif command == "quit":
        print("Thank you for playing. Your score was " + str(score))
        break
    else:
        print("Sorry, I didn't understand.")

