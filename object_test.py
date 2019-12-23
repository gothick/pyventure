object_data = {
    "torch": {
        "name": "an Ever Ready torch",
        "description": "a plastic 1970s Ever Ready torch"
    },
    "iphone": {
        "name": "an iPhone SE",
        "description": "an iPhone SE. It seems to be connected to the house WiFi."
    }
}

room_data = {
    "lounge": {
        "name": "the lounge",
        "objects": { "iphone" },
        "description": "You are in a dusty living room, full to the (peeling) ceiling with stuff.",
        "exits": {
            "north": "kitchen",
            "south": "street"
        }
    },
    "kitchen": {
        "name": "the kitchen",
        "objects": set(),
        "description": "You are in a squalid kitchen. There may be work surfaces somewhere under the pile of mouldering plates and pans, but it's hard to tell.",
        "exits": {
            "south": "lounge",
            "north": "bathroom"
        }
    },
    "street": {
        "name": "Ashgrove Road",
        "objects": set(),
        "description": "You are in a Victorian terraced street in Bristol. It is raining.",
        "exits": {
            "north": "lounge"
            }
        },
    "bathroom": {
        "name": "the bathroom",
        "objects": set(),
        "description": "You are in a dark bathroom. You pull the light cord, and are rewarded with a disappointing 'clunk', and no additional light.",
        "exits": {
            "south": "kitchen"
            }
        }
    }

class Room:
    def __init__(self, name, description, objects, exits):
        self.name = name
        self.description = description
        self.exits = exits
    def __repr__(self):
        return self.name
        
class Object:
    def __init__(self, name, description):
        self.name = name
        self.description = description
    def __repr__(self):
        return self.name

rooms = {}
objects = {}

for room in room_data:
    rooms[room] = Room(room_data[room]["name"],
                       room_data[room]["description"],
                       room_data[room]["objects"],
                       room_data[room]["exits"])

for object in object_data:
    objects[object] = Object(object_data[object]["name"],
                             object_data[object]["description"])

# It all starts here

