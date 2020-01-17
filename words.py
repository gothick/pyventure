from enum import Enum, auto

class Noun(Enum):
    # TODO The doodah is just used for testing; take it out sometime?
    DOODAH = auto()

    # Directions
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()
    UP = auto()
    DOWN = auto()

    # Items
    UNKNOWN = auto() # Represents a noun that's not in our vocabulary
    TORCH = auto()
    PHONE = auto()
    TV = auto()
    PENNY_FARTHING = auto()
    SHIRT = auto()
    PLUS_FOURS = auto()
    FRIDGE = auto()
    MENUS = auto()
    ESPRESSO_MACHINE = auto()
    BATHROOM_CABINET = auto()
    SINK = auto()
    BATH = auto()
    BEARD_OIL = auto()
    BAG = auto()
    BOXER_SHORTS = auto()
    WARDROBE = auto()
    TRUNK = auto()
    BEARD = auto()

# Useful collection of for our special directional nouns
DIRECTIONS = {
    Noun.NORTH: "north", 
    Noun.EAST: "east", 
    Noun.SOUTH: "south", 
    Noun.WEST: "west", 
    Noun.UP: "up", 
    Noun.DOWN: "down"
} 

normalised_nouns = {
    "north": Noun.NORTH,
    "n": Noun.NORTH,
    "east": Noun.EAST,
    "e": Noun.EAST,
    "south": Noun.SOUTH,
    "s": Noun.SOUTH,
    "west": Noun.WEST,
    "w": Noun.WEST,
    "up": Noun.UP,
    "u": Noun.UP,
    "down": Noun.DOWN,
    "d": Noun.DOWN,

    "torch": Noun.TORCH,
    "iphone": Noun.PHONE,
    "iphone se": Noun.PHONE,
    "phone": Noun.PHONE,
    "tv": Noun.TV,
    "television": Noun.TV,
    "pennyfarthing": Noun.PENNY_FARTHING,
    "penny farthing": Noun.PENNY_FARTHING,
    "penny-farthing": Noun.PENNY_FARTHING,
    "bicycle": Noun.PENNY_FARTHING,
    "bike": Noun.PENNY_FARTHING,
    "shirt": Noun.SHIRT,
    "natty shirt": Noun.SHIRT,
    "paisley shirt": Noun.SHIRT,
    "plus fours": Noun.PLUS_FOURS,
    "plus-fours": Noun.PLUS_FOURS,
    "tweed plus fours": Noun.PLUS_FOURS,
    "fridge": Noun.FRIDGE,
    "smeg": Noun.FRIDGE,
    "smeg fridge": Noun.FRIDGE,
    "menus": Noun.MENUS,
    "takeaway menus": Noun.MENUS,
    "espresso machine": Noun.ESPRESSO_MACHINE,
    "machine": Noun.ESPRESSO_MACHINE,
    "espresso": Noun.ESPRESSO_MACHINE,
    "coffee machine": Noun.ESPRESSO_MACHINE,
    "coffee maker": Noun.ESPRESSO_MACHINE,
    "bathroom cabinet": Noun.BATHROOM_CABINET,
    "cabinet": Noun.BATHROOM_CABINET,
    "sink": Noun.SINK,
    "bath": Noun.BATH,
    "gargoyle clawfoot bath": Noun.BATH,
    "clawfoot bath": Noun.BATH,
    "beard oil": Noun.BEARD_OIL,
    "oil": Noun.BEARD_OIL,
    "can": Noun.BEARD_OIL,
    "bag": Noun.BAG,
    "bag of holding": Noun.BAG,
    "boxer shorts": Noun.BOXER_SHORTS,
    "boxers": Noun.BOXER_SHORTS,
    "shorts": Noun.BOXER_SHORTS,
    "wardrobe": Noun.WARDROBE,
    "doodah": Noun.DOODAH,
    "trunk": Noun.TRUNK,
    "wooden trunk": Noun.TRUNK,
    "beard": Noun.BEARD
}

class Verb(Enum):
    RIDE = auto()
    TURN_ON = auto()
    TURN_OFF = auto()
    GO = auto()
    EXAMINE = auto()
    TAKE = auto()
    SCORE = auto()
    INVENTORY = auto()
    DROP = auto()
    QUIT = auto()
    HEALTH = auto()
    # TODO: This is for debugging only
    XYZZY = auto()
    PUT_ON = auto()
    TAKE_OFF = auto()
    OPEN = auto()
    CLOSE = auto()
    COMB = auto()

normalised_verbs = {
    "ride": Verb.RIDE,
    "get on": Verb.RIDE,
    "mount": Verb.RIDE,
    "turn on": Verb.TURN_ON,
    "activate": Verb.TURN_ON,
    "turn off": Verb.TURN_OFF,
    "deactivate": Verb.TURN_OFF,
    "go": Verb.GO,
    "examine": Verb.EXAMINE,
    "look": Verb.EXAMINE,
    "look at": Verb.EXAMINE,
    "l": Verb.EXAMINE,
    "describe": Verb.EXAMINE,
    "take": Verb.TAKE,
    "get": Verb.TAKE,
    "score": Verb.SCORE,
    "inventory": Verb.INVENTORY,
    "i": Verb.INVENTORY,
    "drop": Verb.DROP,
    "quit": Verb.QUIT,
    "health": Verb.HEALTH,
    "xyzzy": Verb.XYZZY,
    "wear": Verb.PUT_ON,
    "put on": Verb.PUT_ON,
    "take off": Verb.TAKE_OFF,
    "remove": Verb.TAKE_OFF,
    "open": Verb.OPEN,
    "close": Verb.CLOSE,
    "comb": Verb.COMB,
    "tidy": Verb.COMB,
    "groom": Verb.COMB
}
