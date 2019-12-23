normalised_verbs = {
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
    "quit": "quit"
}

normalised_nouns = {
    "iphone": "iphone",
    "iphone se": "iphone",
    "phone": "iphone"
}

class Parser:
    def __init__(self, command):
        self.valid = False
        verb = ""
        noun = ""
        space_pos = command.rfind(" ")
        if space_pos == -1:
            verb = command.lower()
        else:
            verb = command[0:space_pos].lower()
            noun = command[space_pos + 1:].lower()

        # Special cases outside our normal grammar:
        if noun == "" and verb in ["n", "s", "e", "w", "u", "d", "up", "down"]:
            noun = {"n": "north", "s": "south", "e": "east", "w": "west", "u": "up", "d": "down", "up": "up", "down": "down"}.get(verb);
            verb = "go"

        if verb in normalised_verbs:
            self.__verb = normalised_verbs[verb]
            self.valid = True

        self.__noun = noun
        # Normalise the noun if we can, but don't worry about it if we can't,
        # and just store what we were given.
        if noun in normalised_nouns:
            self.__noun = normalised_nouns[noun]

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
