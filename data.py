object_data = {
    "torch": {
        "name": "an Ever Ready torch",
        "description":
        {
            "off": "a plastic 1970s Ever Ready torch. It is switched off.",
            "on": "a plastic 1870s Ever Ready torch. It's switched on, and emits a surprising amount of light."
        },
        "states": [ "off", "on" ],
        "verbs": { "turn on": "on", "turn off": "off" },
        "moveable": True
    },
    "iphone": {
        "name": "an iPhone SE",
        "description": {
            "on": "an iPhone SE. It seems to be connected to the house WiFi.",
            "off": "an iPhone SE. The screen is dark. I think it's turned off."
        },
        "states": [ "on", "off" ],
        "verbs": { "turn on": "on", "turn off": "off" },
        "moveable": True
    },
    "remote": {
        "name": "a remote control",
        "description": "a remote control for a JVC Smart TV. It rattles a bit as you shake it.",
        "states": [],
        "verbs": {},
        "moveable": True
    },
    "books": {
        "name": "pile upon dusty pile of books",
        "description": "stacks of books. They don't look stable.",
        "states": [],
        "verbs": {},
        "moveable": False
    },
    "stuff": {
        "name": "stuff. A lot of stuff",
        "description": "just generic stuff, it seems. Have you seen 'Hoarders'?.",
        "states": [],
        "verbs": {},
        "moveable": False
    },
    "tv": {
        "name": "a television",
        "description": "a modern-looking JVC smart TV. It's turned off.",
        "states": [],
        "verbs": {},
        "moveable": False
    }
}

room_data = {
    "lounge": {
        "name": "The lounge",
        "objects": {
            "default": { "iphone", "tv", "stuff" }
        },
        "description": {
            "default": "You are in a dusty living room, full to the (peeling) ceiling with stuff."
        },
        "exits": {
            "north": "hall",
            "south": "street"
        },
        "states": ["default"]
    },
    "hall": {
        "name": "The hall",
        "objects": {
            "default": set()
        },
        "description": {
            "default": "You are in a tiny hallway between the lounge and the kitchen, at the bottom of a flight of stairs"
        },
        "exits": {
            "north": "kitchen",
            "south": "lounge",
            "up": "stairs"
        },
        "states": ["default"]
    },
    "stairs": {
        "name": "The stairs",
        "objects": {
            "default": { "books" }
        },
        "description": {
            "default": "You get halfway up the narrow flight of stairs before the piles of books on either side become too constricting. Perhaps you should go back downstairs before you cause an avalanche."
        },
        "exits": {
            "down": "hall"
        },
        "states": ["default"]
    },
    "kitchen": {
        "name": "The kitchen",
        "objects": {
            "default": set()
        },
        "description": {
            "default": "You are in a squalid kitchen. There may be work surfaces somewhere under the pile of mouldering plates and pans, but it's hard to tell."
        },
        "exits": {
            "north": "bathroom",
            "south": "hall"
        },
        "states": ["default"]
    },
    "street": {
        "name": "Ashgrove Road",
        "objects": {
            "unlit": set(),
            "lit": set()
        },
        "description": {
            "unlit": "You are in a Victorian terraced street in Bristol. It is raining.",
            "lit": "You are in a Victorian terraced street in Bristol. It is raining. The raindrops glint prettily in the cone of light cast by your torch."
        },
        "exits": {
            "north": "lounge"
            },
        "states": ["unlit", "lit"]
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
