object_data = {
    "torch": {
        "name": "an Ever Ready torch",
        "description":
        {
            "off": "a plastic 1970s Ever Ready torch. It is switched off.",
            "on": "a plastic 1870s Ever Ready torch. It's switched on, and emits a surprising amount of light."
        },
        "states": [ "off", "on" ],
        "verbs": { "turn on": "on", "turn off": "off" }
    },
    "iphone": {
        "name": "an iPhone SE",
        "description": {
            "on": "an iPhone SE. It seems to be connected to the house WiFi.",
            "off": "an iPhone SE. The screen is dark. I think it's turned off."
        },
        "states": [ "on", "off" ],
        "verbs": { "turn on": "on", "turn off": "off" }
    },
    "remote": {
        "name": "a remote control",
        "description": "a remote control for a JVC Smart TV. It rattles a bit as you shake it.",
        "states": [],
        "verbs": {}
    }
}

room_data = {
    "lounge": {
        "name": "The lounge",
        "objects": { "iphone" },
        "description": "You are in a dusty living room, full to the (peeling) ceiling with stuff.",
        "exits": {
            "north": "kitchen",
            "south": "street"
        },
        "states": []
    },
    "kitchen": {
        "name": "The kitchen",
        "objects": set(),
        "description": "You are in a squalid kitchen. There may be work surfaces somewhere under the pile of mouldering plates and pans, but it's hard to tell.",
        "exits": {
            "south": "lounge",
            "north": "bathroom"
        },
        "states": []
    },
    "street": {
        "name": "Ashgrove Road",
        "objects": set(),
        "description": "You are in a Victorian terraced street in Bristol. It is raining.",
        "exits": {
            "north": "lounge"
            },
        "states": []
    },
    "bathroom": {
        "name": "The bathroom", 
        "objects": {
            "unlit": set(),
            "lit": { "remote" }
        },
        "description": {
            "unlit": "You are in a dark bathroom. You pull the light cord, and are rewarded with a disappointing 'clunk', and no additional light.",
            "lit": "The torch lights up the bathroom surprisingly well."
        },
        "exits": {
            "south": "kitchen"
        },
        "states": ["unlit", "lit"]
    }
}
