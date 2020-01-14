# New-style item data
item_data = {
    "shirt": {
        "name": "a natty Paisley print shirt",
        "description": "a delightful fitted shirt with a strong Paisley pattern. As you look closely at it your eyes water slightly.",
        "traits": { "moveable", "wearable" } 
    },
    "plusfours": {
        "name": "a pair of tweed plus fours",
        "description": "a pair of tweed plus fours that you claim to have bought from Camden Market, but actually bought on Amazon.",
        "traits": { "moveable", "wearable" }
    },
    "bath": {
        "name": "a gargoyle clawfoot bath",
        "description": "a bath that's far too big for the room, in terms of both size and personality."
    },
    "sink": {
        "name": "a sink",
        "description": "a sink reclaimed from a Victorian pub, with taps to match. You pull on the "
                        "India Pale Ale tap and are rewarded with a stream of hot water."
    },
    "beardoil": {
        "name": "a can of beard oil",
        "description": "a can of patchouli and ylang-ylang beard oil.",
        "traits": "moveable"
    },
    "bathroomcabinet": {
        "type": "StatefulContainerItem",
        "name": "a bathroom cabinet",
        "description": {
            "closed": "a distressed oak bathroom cabinet. Let's face it, you'd be distressed if you had to stare "
                      "at that bath all day long. The cabinet is closed.",
            "open": "a distressed oak bathroom cabinet, standing open."
        },
        "states": [
            "closed",
            "open" 
        ],
        "verbs": { 
            "open": "open", 
            "close": "closed"
        },
        "inventory": {
            "open": ["beardoil"],
            "closed": []
        }
    },
    "fridge": {
        "type": "StatefulItem",
        "name": "a looming Smeg fridge",
        "description": {
            "closed": "a hulking silver giant of a fridge. It seems to be quietly humming a in a smug tone.",
            "open": "a hulking silver giant of a fridge. The door stands open to reveal the white, serene, food-less interior"
        },
        "states": [
            "closed",
            "open"
        ],
        "verbs": {
            "open": "open",
            "close": "closed"
        }
    },
    "espressomachine": {
        "name": "a complicated espresso machine",
        "description": "a designer Italian espresso machine. It looks like what would happen if an Alessi lemon "
                        "juicer and a plumbing supplies store had a baby. Sadly there is no coffee here."
    },
    "menus": {
        "name": "some takeaway menus",
        "description": "a collection of menus from, variously, a vegan slaw shack, a cronut salon and a "
                        "rainbow grilled cheese caravan.",
        "traits": "moveable"
    },
    "iphone": {
        "type": "StatefulItem",
        "name": "the latest iPhone",
        "description": {
            "on": "the latest iPhone. It is approximately size of a tea tray, and seems to be connected to the house WiFi.",
            "off": "the latest iPhone. The screen is dark. I think it's turned off."
        },
        "states": [
            "on", 
            "off" 
        ],
        "verbs": { 
            "turn on": "on", 
            "turn off": "off" 
        },
        "traits": { "moveable" }
    },
    "tv": {
        "name": "a television",
        "description": {
            "off": "a modern-looking Samsung smart TV. It's turned off.",
            "on": "a modern-looking Samsung smart TV. It seems to be showing an episode of Portlandia."
        },
        "states": [
            "off", "on"
        ],
        "verbs": { 
            "turn on": "on", 
            "turn off": "off"
        }
    },
    "pennyfarthing": {
        "name": "a penny-farthing bicycle",
        "description": "a beautifully-restored Victorian penny-farthing with a leather saddle.",
        "traits": { "moveable" }
    }
}

room_data = {
    "livingroom": {
        "name": "The Living Room",
        "inventory": { "iphone", "tv", "pennyfarthing" },
        "description": {
            "basic":  "You are in the living room of a well-kept terraced house. Adorning the walls are "
                        "some post-ironic art prints and a 56\" plasma television. A table made from old "
                        "pallets sits surrounded by red milk crates on the stripped pine floorboards. Light "
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
                        "item": "pennyfarthing",
                        "objection": "The penny-farthing won't fit through there."
                    }
                ]
            },
            "south": { "destination": "street" }
        }
    },
    "bedroom": {
        "name": "The bedroom",
        "description": {
            "basic": "This will be a bedroom, once I've designed it."
        },
        "exits": {
            "north": {"destination": "landing"} 
        }
    },
    "landing": {
        "name": "The upstairs landing",
        "description": {
            "basic": "You are in a tiny landing at the top of a narrow flight of stairs."
        },
        "exits": {
            "north": {"destination": "bathroom"} ,
            "south": {"destination": "bedroom"},
            "down": {
                "destination": "hall",
                "transition": "You tread carefully up a vertiginous flight of stairs. You would "
                              "be gripping a handrail, but your architect told you they were passé."
            }
        }
    },
    "hall": {
        "name": "The hall",
        "description": {
            "basic": "You are in a tiny hallway between the living room and the kitchen, at the bottom of a flight of stairs."
        },
        "exits": {
            "north": {"destination": "kitchen"} ,
            "south": {"destination": "livingroom"},
            "up": {
                "destination": "landing",
                "transition": "You tread carefully down a vertiginous flight of stairs. You would "
                              "be gripping a handrail, but your architect told you they were passé."
            }
        }
    },
    "kitchen": {
        "name": "The kitchen",
        "inventory": { "fridge", "espressomachine", "menus" },
        "description": {
            "basic": "You are in a bijou kitchen that boasts a SMEG fridge, a pile of menus with the Deliveroo logo "
                        "and a complicated-looking espresso machine. There is no actual food to be seen, though there is "
                        " a lingering hint of avocado toast in the air."
        },
        "exits": {
            "south": {"destination": "hall"}
        }
    },
    "street": {
        "name": "The street",
        "description": {
            "basic": "You are in a Victorian terrace in Southville. To the north lies a furniture reclamation yard. From the south "
                     "you hear a distant bass throb from the vinyl stall at the Tobacco Factory market."
        },
        "exits": {
            "north": {"destination": "livingroom"}
        }
    },
    "bathroom": {
        "name": "The bathroom",
        "inventory": { "bath", "sink", "bathroomcabinet" },
        "description": {
            "basic": "You are in a bathroom only just large enough for you, the dominating freestanding bath "
                       "with gargoyle feet and a small white basin which seems to have beer pumps instead of taps. "
                       "Above the basin is a distressed oak bathroom cabinet."
        },
        "exits": {
            "south": {"destination": "landing"}
        }
    }
}
