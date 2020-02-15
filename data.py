from words import Noun, Verb

# Makes the below a bit more semantic
NORTH = Noun.NORTH
EAST  = Noun.EAST
SOUTH = Noun.SOUTH
WEST  = Noun.WEST
UP    = Noun.UP
DOWN  = Noun.DOWN

# Player details
player_data = {
    "start_inventory": {},
    "start_wearing": [Noun.BOXER_SHORTS]
}

# New-style item data
item_data = {
    Noun.BOXER_SHORTS: {
        "name": "a pair of silk polka-dot boxer shorts",
        "description": "a fetching pair of green silk boxer shorts with red polka-dots",
        "traits": { 
            "wearable": {
                "unremoveable": True,
                "unwear_description": "Nobody wants that to happen, trust me."
            }, 
        }
    },
    Noun.PAISLEY_SHIRT: {
        "name": "a natty Paisley print shirt",
        "description": "a delightful fitted shirt with a strong Paisley pattern. As you look closely at it your eyes water slightly.",
        "traits": { "moveable": {}, "wearable": { "slot": "top"} } 
    },
    Noun.Y2_SHIRT: {
        "name": "a Y2 t-shirt.",
        "description": "a faded t-shirt bearing the legend of your favourite band that nobody else has heard of, Y2",
        "traits": { "moveable": {}, "wearable": { "slot": "top" } }
    },
    Noun.PLUS_FOURS: {
        "name": "a pair of tweed plus fours",
        "description": "a pair of tweed plus fours that you claim to have bought from Camden Market, but actually bought on Amazon.",
        "traits": { "moveable": {}, "wearable": { "slot": "bottom" } }
    },
    Noun.HAREM_PANTS: {
        "name": "a pair of fetching purple harem pants",
        "description": "a pair of generously-cut harem pants. They look like they'll be just the job if you get a sudden urge to do the splits.",
        "traits": { "moveable": {}, "wearable": { "slot": "bottom" } }
    },
    Noun.CROCS: {
        "name": "a pair of yellow Crocs",
        "description": "a pair of yellow Crocs, somewhat beaten up from being worn around the house.",
        "traits": { "moveable": {}, "wearable": { "slot": "feet" } }
    },
    Noun.DOC_MARTENS: {
        "name": "a pair of Doc Marten boots",
        "description": "a gorgeous pair of opalescent Doc Martens, recently polished and clearly loved.",
        "traits": { "moveable": {}, "wearable": { "slot": "feet" } }
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
        "traits": { 
            "moveable": {}, 
            "wearable": {
                "unremoveable": True,
                "wear_description": "You apply the beard oil to your wild facial hair.",
                "unwear_description": "You can't put the genie back in the bottle. Or the beard oil, for that matter."
            }
        }
    },    
    Noun.COMB: {
        "name": "a beard comb",
        "description": "a tortoiseshell beard comb. You might need some oil with that.",
        "traits": { "moveable": {} }
    },    
    Noun.BATHROOM_CABINET: {
        "type": "StatefulContainerItem",
        "name": "a bathroom cabinet",
        "description": {
            "closed": "a distressed oak bathroom cabinet. Let's face it, you'd be distressed if you had to stare "
                      "at that bath all day long. The cabinet is closed.",
            "open": "a distressed oak bathroom cabinet, standing open."
        },
        "reflective": {
            "reflective_item_description": "Peeking into the cabinet mirror"
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
                        "The door is closed.",
            "open": "a vintage wardrobe. The door stands open."
        },
        "reflective": {
            "reflective_item_description": "Staring into the wardrobe's distorting mirror"
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
            },
            Verb.ENTER: {
                "message": "What do you think this is, magical realism?"
            }
        },
        "inventory": {
            "open": [ Noun.PLUS_FOURS, Noun.HAREM_PANTS, Noun.PAISLEY_SHIRT, Noun.Y2_SHIRT ],
            "closed": []
        }
    },
    Noun.DRESSING_TABLE: {
        "type": "StatefulContainerItem",
        "name": "a dressing table",
        "description": {
            "closed": "an upcycled Formica dressing table with a single drawer. The drawer is closed.",
            "open": "an upcycled Formica dressing table with a single drawer. The drawer is open."
        },
        "states": [
            "closed",
            "open" 
        ],
        "verbs": {
            Verb.OPEN: {
                "new_state": "open",
                "message": "You open the Formica dressing table drawer."
            },
            Verb.CLOSE: {
                "new_state": "closed",
                "message": "You close the Formica dressing table drawer."
            }
        },
        "inventory": {
            "open": [ Noun.COMB ],
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
            "open": [Noun.DOC_MARTENS, Noun.CROCS],
            "closed": []
        }
    },
    Noun.FRIDGE: {
        "type": "StatefulItem",
        "name": "a looming Smeg fridge",
        "description": {
            "closed": "a hulking silver giant of a fridge. It seems to be quietly humming a in a smug tone.",
            "open": "a hulking silver giant of a fridge. The door stands open to reveal the white, serene, food-less interior. It hums quietly."
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
        "traits": { "moveable": {} }
    },
    Noun.MAGAZINES: {
        "name": "some magazines",
        "description": "some magazines including VICE, AnOther and Wallpaper*. Towards the bottom of the pile, as "
            "if hidden in shame, are some copies Heat and a TV Times.",
        "traits": { "moveable": {} }
    },
    Noun.PHONE: {
        "type": "StatefulItem",
        "name": "the latest iPhone",
        "description": {
            "locked": "the latest iPhone. It is approximately size of a tea tray. It is locked. Its lock screen shows a delicious "
                "cortado, which makes you crave a coffee.",
            "unlocked": "the latest iPhone. It's unlocked. There seem to be applications for Whuzz Skootaz, TODO...",
            "off": "the latest iPhone. The screen is dark. I think it's turned off."
        },
        "states": [
            "off", 
            "locked",
            "unlocked"
        ],
        "verbs": {
            Verb.TURN_ON: {
                "new_state": "locked",
                "message": "After half a minute, the Apple logo is replaced with a lock screen. It shows a picture of "
                            "you and your loved one, which is to say, a cortado served at exactly 54°C in a small "
                            "laboratory beaker.",
                "rules": [
                    {
                        "type": "current_state",
                        "states": ["off"],
                        "message": "It's already on."
                    }
                ]
            },
            Verb.TURN_OFF: {
                "new_state": "off",
                "message": "The Apple[tm] logo briefly appears as you turn off the iPhone[tm], then the screen fades to black.",
                "rules": [
                    {
                        "type": "current_state",
                        "states": ["locked", "unlocked"],
                        "message": "It's already off."
                    }
                ]
            },
            Verb.UNLOCK: {
                "new_state": "unlocked",
                "message": "The phone recognises your handsome, well-groomed beard and tasteful zero-prescription glasses and unlocks at a glance.",
                "requires_extras": { "player_appearance_level" },
                "rules": [
                    {
                        "type": "current_state",
                        "states": ["locked"],
                        "message": "It would have to be locked for you to do that."
                    },
                    {
                       "type": "not_below_appearance_level",
                       "level": 100,
                       "message": "The phone doesn't seem to recognise you. You're not sure if it's the wild beard, the bloodshot eyes or the lack of your usual man-bun and tortoiseshell spectacles that is causing it a problem."
                    }
                ]
            },
            Verb.LOCK: {
                "new_state": "locked",
                "message": "You lock the phone.",
                "rules": [
                    {
                        "type": "current_state",
                        "states": ["unlocked"],
                        "message": "It would have to be unlocked for you to do that."
                    }
                ]
            }
        },
        "traits": { "moveable": {} }
    },
    Noun.TV: {
        "type": "StatefulItem",
        "name": "a television",
        "description": {
            "off": "a modern-looking Samsung smart TV. It's turned off.",
            "on": "a modern-looking Samsung smart TV. It seems to be showing an episode of Portlandia."
        },
        "states": [
            "off", "on"
        ],
        "verbs": { 
            Verb.TURN_ON: {
                "new_state": "on",
                "message": "You turn on the TV. I think you're halfway thorugh an episode of Portlandia."
            },
            Verb.TURN_OFF: {
                "new_state": "off",
                "message": "You turn off the TV."
            }
        }
    },
    Noun.PENNY_FARTHING: {
        "name": "a penny-farthing bicycle",
        "description": "a beautifully-restored Victorian penny-farthing with a leather saddle.",
        "traits": { "moveable": {}, "rideable": {} }
    },
    Noun.RECORDS: {
        "type": "SimpleVerbableItem",
        "name": "a small stack of vinyl records",
        "description": "a stack of vinyl records from your favourite bands that nobody else has heard of, like Plugh, Y2, and the Xyzzy Plovers.",
        "verbs": {
            Verb.PLAY: {
                "type": "random",
                "messages": [
                    "You pluck out the Y2 album at random and put it on the turntable. It's actually surprisingly good.",
                    "You pluck out the Plugh album at random and put it on the turntable. You very quickly take it back off, reminded that there's a reason not many people have heard of them.",
                    "You pluck out the Xyzzy Plovers album at random and put it on the turntable. You very quickly take it back off, reminded that there's a reason not many people have heard of them."
                ]
            }
        }
    },
    Noun.TURNTABLE: {
        "name": "a record player",
        "description": "a vintage Dynatron record player in a teak cabinet."
    }
}

room_data = {
    "livingroom": {
        "name": "The Living Room",
        "inventory": [ Noun.PHONE, Noun.TV, Noun.PENNY_FARTHING, Noun.MAGAZINES ],
        "rules": {
            "can_ride": (False, "You can't ride that in here!")
        },
        "description": {
            "basic":  "You are in the living room of a well-kept terraced house. Adorning the walls are "
                        "some post-ironic art prints and a 56\" plasma television. A table made from old "
                        "pallets sits surrounded by red milk crates on the stripped pine floorboards. Light "
                        "streams in through the picture window from the tidy Southville street outside.",
            "extras": [
                {
                    "type": "if_in_room",
                    "object": Noun.MAGAZINES,
                    "text": "Some magazines lie on the table."
                },
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
                        # We don't want to let the player carry the penny-farthing into
                        # the house. 
                        "type": "not_if_carrying",
                        "item": Noun.PENNY_FARTHING,
                        "objection": "The penny-farthing won't fit through there."
                    }
                ]
            },
            SOUTH: { 
                "destination": "street",
                "rules": [
                    {
                        "type": "only_if_dressed",
                        "objection": "You can't go outside dressed like that! (Hint: type 'inventory', or just 'i' to list your posessions and clothing.)"
                    },
                    {
                        "type": "only_if_shod",
                        "objection": "You'll need to put something on your feet first. It's a rough old world out there."
                    }
                ]
            }
        }
    },
    "diningroom": {
        "name": "The dining room",
        "inventory": [ Noun.TURNTABLE, Noun.RECORDS ],
        "rules": {
            "can_ride": (False, "You can't ride that in here!")
        },
        "description": {
            "basic": "You find yourself in a small dining room, though the varied amateur taxidermy "
                    "in strategically-placed glass cases would probably be enough to put most "
                    "people off their dinner. On the far side of the empty dining table is a teak " 
                    "cabinet with a vintage turntable and some vinyl records.",
            "extras": [
                {
                    "type": "random",
                    "texts": [
                        "A stuffed squirrel gives you a particularly beady look.",
                        "A stuffed badger seems to gnash at the air, as if in pain.",
                        "A stuffed owl's glassy eyes regard you with contempt."
                    ]
                }
            ]
        },
        "exits": {
            NORTH: { "destination": "kitchen" },
            SOUTH: { "destination": "hall" }
        }
    },
    "bedroom": {
        "name": "The bedroom",
        "inventory": [ Noun.WARDROBE, Noun.TRUNK, Noun.DRESSING_TABLE ],
        "rules": {
            "can_ride": (False, "You can't ride that in here!")
        },
        "description": {
            "basic": "You are in a cool bedroom. The single bed hangs like a child's swing from "
                    "ropes that drop from the ceiling. One wall has a cuboid bookcase with no books, "
                    "but instead a varied selection of terraria containing alien-looking succulents "
                    "and cacti. On the far side of the room stand a wardrobe and a large wooden trunk. "
                    "A Formica dressing table sits next to the bed, under the window.",
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
        "rules": {
            "can_ride": (False, "You can't ride that in here!")
        },
        "description": {
            "basic": "You are in a tiny landing at the top of a narrow flight of stairs."
        },
        "exits": {
            NORTH: {"destination": "bathroom"} ,
            SOUTH: {"destination": "bedroom"},
            DOWN: {
                "destination": "hall",
                "transition": "You tread carefully down a vertiginous flight of stairs. You would "
                              "be gripping a handrail, but your architect told you they were passé."
            }
        }
    },
    "hall": {
        "name": "The hall",
        "rules": {
            "can_ride": (False, "You can't ride that in here!")
        },
        "description": {
            "basic": "You are in a tiny hallway between the living room and the dining room, at the bottom of a flight of stairs."
        },
        "exits": {
            Noun.NORTH: {"destination": "diningroom"} ,
            Noun.SOUTH: {"destination": "livingroom"},
            Noun.UP: {
                "destination": "landing",
                "transition": "You tread carefully up a vertiginous flight of stairs. You would "
                              "be gripping a handrail, but your architect told you they were passé."
            }
        }
    },
    "kitchen": {
        "name": "The kitchen",
        "inventory": [ Noun.FRIDGE, Noun.ESPRESSO_MACHINE, Noun.MENUS ],
        "rules": {
            "can_ride": (False, "You can't ride that in here!")
        },
        "description": {
            "basic": "You are in a bijou kitchen that boasts a SMEG fridge, a pile of menus with the Deliveroo logo "
                        "and a complicated-looking espresso machine. There is no actual food to be seen, though there is "
                        "a lingering hint of avocado toast in the air."
        },
        "exits": {
            SOUTH: {"destination": "diningroom"}
        }
    },
    "street": {
        "name": "The street",
        "description": {
            "basic": "You are in a Victorian terrace in Southville. To the north lies a furniture reclamation yard. From the south "
                     "you hear a distant bass throb from the vinyl stall at the Tobacco Factory market."
        },
        "rules": {
            "nudity": (False, "In public!? You're a hipster, not a flasher.")
        },
        "exits": {
            NORTH: {
                "destination": "livingroom",
                "rules": [
                    {
                        "type": "not_if_riding",
                        "item": Noun.PENNY_FARTHING,
                        "objection": "You can't ride into the house on a penny-farthing!"
                    }
                ]
            },
            EAST: {
                "destination": "streetmaze_d"
            },
            WEST: {
                "destination": "streetmaze_c"
            }
        }
    },
    "streetmaze_a": {
        "name": "The street",
        "description": {
            "basic": "You are in a maze of twisty Victorian streets, all looking alike."
        },
        "exits": {
            NORTH: {
                "destination": "streetmaze_g"
            },
            SOUTH: {
                "destination": "streetmaze_d"
            },
            EAST: {
                "destination": "streetmaze_b"
            },
            WEST: {
                "destination": "streetmaze_c"
            },
        }
    },
    "streetmaze_b": {
        "name": "The street",
        "description": {
            "basic": "You are in a twisty maze of Victorian streets, all looking alike."
        },
        "exits": {
            NORTH: {
                "destination": "streetmaze_h"
            },
            SOUTH: {
                "destination": "streetmaze_e"
            },
            EAST: {
                "destination": "streetmaze_c"
            },
            WEST: {
                "destination": "streetmaze_a"
            },
        }
    },
    "streetmaze_c": {
        "name": "The street",
        "description": {
            "basic": "You are in a maze of twisty Victorian streets, looking all alike."
        },
        "exits": {
            NORTH: {
                "destination": "streetmaze_i"
            },
            SOUTH: {
                "destination": "streetmaze_f"
            },
            EAST: {
                "destination": "street"
            },
            WEST: {
                "destination": "streetmaze_b"
            },
        }
    },
    "streetmaze_d": {
        "name": "The street",
        "description": {
            "basic": "You are in a twisty maze of Victorian streets, looking all alike."
        },
        "exits": {
            NORTH: {
                "destination": "streetmaze_a"
            },
            SOUTH: {
                "destination": "streetmaze_g"
            },
            EAST: {
                "destination": "streetmaze_e"
            },
            WEST: {
                "destination": "street"
            },
        }
    },
    "streetmaze_e": {
        "name": "The street",
        "description": {
            "basic": "You are in a twisted maze of Victorian streets, all looking alike."
        },
        "exits": {
            NORTH: {
                "destination": "streetmaze_b"
            },
            SOUTH: {
                "destination": "streetmaze_h"
            },
            EAST: {
                "destination": "streetmaze_f"
            },
            WEST: {
                "destination": "streetmaze_d"
            },
        }
    },
    "streetmaze_f": {
        "name": "The street",
        "description": {
            "basic": "You are in a twisted maze of Victorian streets, looking all alike."
        },
        "exits": {
            NORTH: {
                "destination": "streetmaze_c"
            },
            SOUTH: {
                "destination": "streetmaze_i"
            },
            EAST: {
                "destination": "streetmaze_d"
            },
            WEST: {
                "destination": "streetmaze_e"
            },
        }
    },
    "streetmaze_g": {
        "name": "The street",
        "description": {
            "basic": "You are in a twisting maze of Victorian streets, all looking alike."
        },
        "exits": {
            NORTH: {
                "destination": "streetmaze_d"
            },
            SOUTH: {
                "destination": "streetmaze_a"
            },
            EAST: {
                "destination": "streetmaze_h"
            },
            WEST: {
                "destination": "streetmaze_i"
            },
        }
    },
    "streetmaze_h": {
        "name": "The street",
        "description": {
            "basic": "You are in a maze of twisting Victorian streets, looking all alike."
        },
        "exits": {
            NORTH: {
                "destination": "streetmaze_e"
            },
            SOUTH: {
                "destination": "streetmaze_b"
            },
            EAST: {
                "destination": "streetmaze_i"
            },
            WEST: {
                "destination": "streetmaze_g"
            },
        }
    },
    "streetmaze_i": {
        "name": "The street",
        "description": {
            "basic": "You are lost in a maze of twisty Victorian streets, all looking alike."
        },
        "exits": {
            NORTH: {
                "destination": "streetmaze_f"
            },
            SOUTH: {
                "destination": "streetmaze_c"
            },
            EAST: {
                "destination": "streetmaze_g"
            },
            WEST: {
                "destination": "streetmaze_h"
            },
        }
    },
    "bathroom": {
        "name": "The bathroom",
        "inventory": [ Noun.BATH, Noun.SINK, Noun.BATHROOM_CABINET ],
        "rules": {
            "can_ride": (False, "You can't ride that in here!")
        },
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
