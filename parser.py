normalised_verbs = {
    "ride": "ride",
    "get on": "ride",
    "mount": "ride",
    "turn on": "turn on",
    "activate": "turn on",
    "turn off": "turn off",
    "deactivate": "turn off",
    "go": "go",
    "examine": "examine",
    "look": "examine",
    "describe": "examine",
    "take": "take",
    "get": "take",
    "score": "score",
    "inventory": "inventory",
    "i": "inventory",
    "drop": "drop",
    "quit": "quit",
    "health": "health",
    "xyzzy": "xyzzy"
}

# Special case abbreviations. We'll turn these into GO commands
directions = {
    "n":     "north",
    "north": "north",
    "s":     "south",
    "south": "south",
    "e":     "east",
    "east":  "east",
    "w":     "west",
    "west":  "west",
    "u":     "up",
    "up":    "up",
    "d":     "down",
    "down":  "down"
}

normalised_nouns = {
    "iphone": "iphone",
    "torch": "torch",
    "iphone se": "iphone",
    "phone": "iphone",
    "tv": "tv",
    "television": "tv",
    "pennyfarthing": "pennyfarthing",
    "penny farthing": "pennyfarthing",
    "penny-farthing": "pennyfarthing",
    "bicycle": "pennyfarthing",
    "bike": "pennyfarthing"
}

class Parser:
    def tokenise(self, command):
        verb = None
        noun = None
        words = command.lower().split(None, 2)
        if len(words) == 1:
            # If it's a direction instruction abbreviate we'll turn it
            # into a full-on go command
            if words[0] in directions:
                return ("go", directions[words[0]])

            # Looking for a verb only.
            return (normalised_verbs.get(words[0]), None)
        elif len(words) == 2:
            # Simple split verb-noun:
            return (normalised_verbs.get(words[0]), normalised_nouns.get(words[1]))
        else:
            # We must have 3, as we passed maxsplit to split() above
            tryverb = words[0] + " " + words[1]
            trynoun = words[2]
            if tryverb in normalised_verbs:
                tryverb = normalised_verbs[tryverb]
                if trynoun in normalised_nouns:
                    trynoun = normalised_nouns[trynoun]
                return (tryverb, trynoun)
            else:
                tryverb = words[0]
                trynoun = words[1] + " " + words[2]
                if tryverb in normalised_verbs:
                    tryverb = normalised_verbs[tryverb]
                    # We try to normalise the noun if we can, but if we can't we
                    # leave it raw.
                    if trynoun in normalised_nouns:
                        trynoun = normalised_nouns[trynoun]
                    return (tryverb, trynoun)
        # Fallthrough
        return (None, None)

    def __init__(self, command):
        self.valid = False

        (verb, noun) = self.tokenise(command)
        if verb:
            self.__verb = verb
            self.valid = True

        self.__noun = noun


    @property
    def verb(self):
        if self.valid:
            return self.__verb
        else:
            raise Exception("Attempt to read from invalid Parser")
    @property
    def noun(self):
        if self.valid:
            return self.__noun
        else:
            raise Exception("Attempt to read from invalid Parser")
