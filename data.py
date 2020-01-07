object_data = {
    "torch": {
        "name": "an Ever Ready torch",
        "description":
        {
            "off": "a plastic 1970s Ever Ready torch. It is switched off.",
            "on": "a plastic 1970s Ever Ready torch. It's switched on, and emits a surprising amount of light."
        },
        "states": [ "off", "on" ],
        "verbs": { "turn on": "on", "turn off": "off" },
        "moveable": True
    },
    "iphone": {
        "name": "the latest iPhone",
        "description": {
            "on": "the latest iPhone. It is approximately size of a tea tray, and seems to be connected to the house WiFi.",
            "off": "the latest iPhone. The screen is dark. I think it's turned off."
        },
        "states": [ "on", "off" ],
        "verbs": { "turn on": "on", "turn off": "off" },
        "moveable": True
    },
    "plusfours": {
        "name": "a pair of tweed plus fours",
        "description": {
            "default": "a pair of tweed plus fours that you claim to have bought from Camden Market, but actually bought on Amazon."
        },
        "states": [ "default" ],
        "verbs": {},
        "moveable": True,
        "wearable": True
    },
    "remote": {
        "name": "a remote control",
        "description": {
            "default": "a remote control for a JVC Smart TV. It rattles a bit as you shake it."
        },
        "states": [ "default" ],
        "verbs": {},
        "moveable": True
    },
    "books": {
        "name": "pile upon dusty pile of books",
        "description": {
            "default": "stacks of books. They don't look stable."
        },
        "states": [ "default"],
        "verbs": {},
        "moveable": False
    },
    "stuff": {
        "name": "stuff. A lot of stuff",
        "description": {
            "default": "just generic stuff, it seems. Have you seen 'Hoarders'?."
        },
        "states": ["default"],
        "verbs": {},
        "moveable": False
    },
    "tv": {
        "name": "a television",
        "description": {
            "off": "a modern-looking Samsung smart TV. It's turned off.",
            "on": "a modern-looking Samsung smart TV. It seems to be showing an episode of Portlandia."
        },
        "states": {"off", "on"},
        "verbs": { "turn on": "on", "turn off": "off"},
        "moveable": False
    },
    "pennyfarthing": {
        "name": "a penny-farthing bicycle",
        "description": {
            "default": "a beautifully-restored Victorian penny-farthing with a leather saddle."
        },
        "states": ["default"],
        "verbs": {},
        "moveable": True
    }
}

room_data = {
    "livingroom": {
        "name": "The Living Room",
        "objects": {
            "default": { "iphone", "tv", "pennyfarthing" }
        },
        "description": {
            "default":  "You are in the living room of a well-kept terraced house. Adorning the walls are "
                        "some post-ironic art prints and a 56\" plasma television. A table made from old "
                        "pallets sits surrounded by milk crates on the stripped pine floorboards. Light "
                        "streams in through the picture window from the tidy Southville street outside.",
            "extras": [
                {
                    "type": "if_in_room",
                    "object": "pennyfarthing",
                    "text": " By the front door rests a penny-farthing bicycle."
                }
            ]
        },
        "exits": {
            "north": {
                "destination": "hall",
                "rules": [
                    {
                        "type": "not_if_carrying",
                        "object": "pennyfarthing",
                        "objection": "The penny-farthing won't fit through there."
                    }
                ]
            },
            "south": { "destination": "street" }
        },
        "states": ["default"]
    },
    "hall": {
        "name": "The hall",
        "objects": {
            "default": set()
        },
        "description": {
            "default": "You are in a tiny hallway between the living room and the kitchen, at the bottom of a flight of stairs."
        },
        "exits": {
            "north": {"destination": "kitchen"} ,
            "south": {"destination": "livingroom"},
            "up": {"destination": "stairs"}
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
            "down": {"destination": "hall"}
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
            "north": {"destination": "bathroom"},
            "south": {"destination": "hall"}
        },
        "states": ["default"]
    },
    "street": {
        "name": "The street",
        "objects": {
            "default": set()
        },
        "description": {
            "default": "You are in a Victorian terrace in Southville. To the north lies a furniture reclamation yard. From the south "
                     "you hear a distant bass throb from the vinyl stall at the Tobacco Factory market."
        },
        "exits": {
            "north": {"destination": "livingroom"}
            },
        "states": ["default"]
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
            "south": {"destination": "kitchen"}
        },
        "states": ["unlit", "lit"]
    }
}
