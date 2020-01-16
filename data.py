from words import Noun, Verb

# Makes the below a bit more semantic
NORTH = Noun.NORTH
EAST  = Noun.EAST
SOUTH = Noun.SOUTH
WEST  = Noun.WEST
UP    = Noun.UP
DOWN  = Noun.DOWN

# New-style item data
item_data = {
    Noun.BOXER_SHORTS: {
        "name": "a pair of silk polka-dot boxer shorts",
        "description": "a fetching pair of green silk boxer shorts with red polka-dots",
        "traits": { "wearable" }
    },
    Noun.DOODAH: {
        "name": "a doodah",
        "description": "a doodah. You know, a bit like a thingummy, only heavier.",
        "traits": { "moveable" }
    },
    Noun.SHIRT: {
        "name": "a natty Paisley print shirt",
        "description": "a delightful fitted shirt with a strong Paisley pattern. As you look closely at it your eyes water slightly.",
        "traits": { "moveable", "wearable" } 
    },
    Noun.PLUS_FOURS: {
        "name": "a pair of tweed plus fours",
        "description": "a pair of tweed plus fours that you claim to have bought from Camden Market, but actually bought on Amazon.",
        "traits": { "moveable", "wearable" }
    },
    Noun.BATH: {
        "name": "a gargoyle clawfoot bath",
        "description": "a bath that's far too big for the room, in terms of both size and personality."
    },
    Noun.SINK: {
        "name": "a sink",
        "description": "a sink reclaimed from a Victorian pub, with taps to match. You pull on the "
                        "India Pale Ale tap and are rewarded with a stream of hot water."
    },
    Noun.BEARD_OIL: {
        "name": "a can of beard oil",
        "description": "a can of patchouli and ylang-ylang beard oil.",
        "traits": "moveable"
    },    
    Noun.BATHROOM_CABINET: {
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
            Verb.OPEN: {
                "new_state": "open",
                "message": "You open the bathroom cabinet door."
            },
            Verb.CLOSE: {
                "new_state": "closed",
                "message": "The cabinet door whips shut on self-closing hinges and nearly takes your finger off in the process."
            }
        },
        "inventory": {
            "open": [ Noun.BEARD_OIL ],
            "closed": []
        }
    },
    Noun.WARDROBE: {
        "type": "StatefulContainerItem",
        "name": "a wardobe",
        "description": {
            "closed": "a vintage wardrobe with a distorting fairground mirror fixed to the front. "
                        "It makes your hangover look worse.",
            "open": "a vintage wardrobe. The door stands open."
        },
        "states": [
            "closed",
            "open" 
        ],
        "verbs": {
            Verb.OPEN: {
                "new_state": "open",
                "message": "You open the wardrobe. The hinges creak a bit."
            },
            Verb.CLOSE: {
                "new_state": "closed",
                "message": "You close the wardrobe door and scare yourself a bit when your distorted reflection reappears."
            }
        },
        "inventory": {
            "open": [ Noun.PLUS_FOURS ],
            "closed": []
        }
    },
    Noun.TRUNK: {
        "type": "StatefulContainerItem",
        "name": "a large wooden trunk",
        "description": {
            "closed": "a large wooden trunk, which from a distance appears to be upcycled "
                        "Victoriana, but on closer inspection looks quite cheap and probably "
                        "came from Argos.",
            "open": "a large wooden trunk. The lid stands open."
        },
        "states": [
            "closed",
            "open" 
        ],
        "verbs": {
            Verb.OPEN: {
                "new_state": "open",
                "message": "You open the trunk."
            },
            Verb.CLOSE: {
                "new_state": "closed",
                "message": "You close the trunk."
            }
        },
        "inventory": {
            "open": [Noun.DOODAH],
            "closed": []
        }
    },
    Noun.FRIDGE: {
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
            Verb.OPEN: {
                "new_state": "open",
                "message": "You open the fridge to reveal... a gleaming, white, spacious, elegant and completely empty interior."
            },
            Verb.CLOSE: {
                "new_state": "closed",
                "message": "The fridge door swings shut with an expensive-sounding swoosh."
            }
        }
    },
    Noun.ESPRESSO_MACHINE: {
        "name": "a complicated espresso machine",
        "description": "a designer Italian espresso machine. It looks like what would happen if an Alessi lemon "
                        "juicer and a plumbing supplies store had a baby. Sadly there is no coffee here."
    },
    Noun.MENUS: {
        "name": "some takeaway menus",
        "description": "a collection of menus from, variously, a vegan slaw shack, a cronut salon and a "
                        "rainbow grilled cheese caravan.",
        "traits": "moveable"
    },
    Noun.PHONE: {
        "type": "StatefulItem",
        "name": "the latest iPhone",
        "description": {
            "on": "the latest iPhone. It is approximately size of a tea tray, and seems to be connected to the house WiFi.",
            "off": "the latest iPhone. The screen is dark. I think it's turned off."
        },
        "states": [
            "off", 
            "on" 
        ],
        "verbs": {
            Verb.TURN_ON: {
                "new_state": "on",
                "message": "After half a minute, the Apple logo is replaced with a lock screen. It shows a picture of "
                            "you and your loved one, which is to say, a cortado served at exactly 54°C in a small "
                            "laboratory beaker."
            },
            Verb.TURN_OFF: {
                "new_state": "off",
                "message": "The Apple[tm] logo briefly appears as you turn off the iPhone[tm], then the screen fades to black."
            }
        },
        "traits": { "moveable" }
    },
    Noun.TV: {
        "name": "a television",
        "description": {
            "off": "a modern-looking Samsung smart TV. It's turned off.",
            "on": "a modern-looking Samsung smart TV. It seems to be showing an episode of Portlandia."
        },
        "states": [
            "off", "on"
        ],
        "verbs": { 
            Verb.TURN_ON: "on", 
            Verb.TURN_OFF: "off"
        }
    },
    Noun.PENNY_FARTHING: {
        "name": "a penny-farthing bicycle",
        "description": "a beautifully-restored Victorian penny-farthing with a leather saddle.",
        "traits": { "moveable" }
    }
}

room_data = {
    "livingroom": {
        "name": "The Living Room",
        "inventory": { Noun.PHONE, Noun.TV, Noun.PENNY_FARTHING },
        "description": {
            "basic":  "You are in the living room of a well-kept terraced house. Adorning the walls are "
                        "some post-ironic art prints and a 56\" plasma television. A table made from old "
                        "pallets sits surrounded by red milk crates on the stripped pine floorboards. Light "
                        "streams in through the picture window from the tidy Southville street outside.",
            "extras": [
                {
                    "type": "if_in_room",
                    "object": Noun.PENNY_FARTHING,
                    "text": "By the front door rests a penny-farthing bicycle."
                }
            ]
        },
        "exits": {
            NORTH: {
                "destination": "hall",
                "rules": [
                    {
                        "type": "not_if_carrying",
                        "item": Noun.PENNY_FARTHING,
                        "objection": "The penny-farthing won't fit through there."
                    }
                ]
            },
            SOUTH: { "destination": "street" }
        }
    },
    "bedroom": {
        "name": "The bedroom",
        "inventory": { Noun.WARDROBE, Noun.TRUNK },
        "description": {
            "basic": "You are in a cool bedroom. The single bed hangs like a child's swing from "
                    "ropes that drop from the ceiling. One wall has a cuboid bookcase with no books, "
                    "but instead a varied selection of terraria containing alien-looking succulents "
                    "and cacti. On the far side of the room stand a wardrobe and a large wooden trunk.",
            "extras": [
                {
                    "type": "random",
                    "texts": [ 
                        "A framed picture on the wall depicts a bespectacled giraffe smoking a pipe.",
                        "A framed picture on the wall depicts a fox with a handlebar moustache.",
                        "A framed picture on the wall depicts a flamingo wearing a top hat."
                    ]

                }
            ]
        },
        "exits": {
            NORTH: {"destination": "landing"} 
        }
    },
    "landing": {
        "name": "The upstairs landing",
        "description": {
            "basic": "You are in a tiny landing at the top of a narrow flight of stairs."
        },
        "exits": {
            NORTH: {"destination": "bathroom"} ,
            SOUTH: {"destination": "bedroom"},
            DOWN: {
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
            Noun.NORTH: {"destination": "kitchen"} ,
            Noun.SOUTH: {"destination": "livingroom"},
            Noun.UP: {
                "destination": "landing",
                "transition": "You tread carefully down a vertiginous flight of stairs. You would "
                              "be gripping a handrail, but your architect told you they were passé."
            }
        }
    },
    "kitchen": {
        "name": "The kitchen",
        "inventory": { Noun.FRIDGE, Noun.ESPRESSO_MACHINE, Noun.MENUS },
        "description": {
            "basic": "You are in a bijou kitchen that boasts a SMEG fridge, a pile of menus with the Deliveroo logo "
                        "and a complicated-looking espresso machine. There is no actual food to be seen, though there is "
                        " a lingering hint of avocado toast in the air."
        },
        "exits": {
            SOUTH: {"destination": "hall"}
        }
    },
    "street": {
        "name": "The street",
        "description": {
            "basic": "You are in a Victorian terrace in Southville. To the north lies a furniture reclamation yard. From the south "
                     "you hear a distant bass throb from the vinyl stall at the Tobacco Factory market."
        },
        "exits": {
            NORTH: {"destination": "livingroom"}
        }
    },
    "bathroom": {
        "name": "The bathroom",
        "inventory": { Noun.BATH, Noun.SINK, Noun.BATHROOM_CABINET },
        "description": {
            "basic": "You are in a bathroom only just large enough for you, the dominating freestanding bath "
                       "with gargoyle feet and a small white basin which seems to have beer pumps instead of taps. "
                       "Above the basin is a distressed oak bathroom cabinet."
        },
        "exits": {
            SOUTH: {"destination": "landing"}
        }
    }
}
