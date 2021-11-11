class PyvParser:
    def __init__(
            self, 
            vocab_nouns, 
            unknown_noun, 
            vocab_verbs, 
            go_verb,
            vocab_directions, 
            normalised_nouns, 
            normalised_verbs
    ):
        self.vocab_nouns = vocab_nouns
        self.vocab_verbs = vocab_verbs
        self.vocab_directions = vocab_directions
        self.normalised_nouns = normalised_nouns
        self.normalised_verbs = normalised_verbs
        self.UNKNOWN_NOUN = unknown_noun
        self.GO_VERB = go_verb

    def noun_string_to_token(self, noun_string):
        noun = self.normalised_nouns.get(noun_string)
        if not noun:
            noun = self.UNKNOWN_NOUN
        return noun
    
    def verb_string_to_token(self, verb_string):
        # It a parsing error if we don't find a verb at the 
        # moment, so I'm just going to return None if we didn't
        # find anything.
        return self.normalised_verbs.get(verb_string)

    # Returns (Verb, Noun)
    def tokenise(self, command):
        words = command.lower().split(None)

        # Srip out articles
        words = list(filter(lambda word: word not in [ "the", "a", "an" ] , words))

        if len(words) == 0:
            return(None, None)
        if len(words) == 1:
            # If it's a direction instruction abbreviate we'll turn it
            # into a full-on go command
            noun = self.noun_string_to_token(words[0])
            if noun in self.vocab_directions: # North, East, etc.
                return (self.GO_VERB, noun)

            # Our single word wasn't one of our expected nouns, so let's hope
            # it's a sensible standalone verb, like "LOOK"
            return (self.verb_string_to_token(words[0]), None)
        elif len(words) == 2:
            # Simple split verb-noun:
            return (self.verb_string_to_token(words[0]), self.noun_string_to_token(words[1]))
        elif len(words) == 3:
            # For three words we may have a two-word noun or a two-word verb
            tryverb = self.verb_string_to_token(words[0] + " " + words[1])
            trynoun = self.noun_string_to_token(words[2])
            if tryverb:
                return (tryverb, trynoun)
            else:
                tryverb = self.verb_string_to_token(words[0])
                trynoun = self.noun_string_to_token(words[1] + " " + words[2])
                if tryverb:
                    return (tryverb, trynoun)
        else:
            # Going to try a two-word verb and a two-word noun, then we're out
            # of ideas.
            tryverb = self.verb_string_to_token(words[0] + " " + words[1])
            trynoun = self.noun_string_to_token(words[2] + " " + words[3])
            if tryverb:
                return(tryverb, trynoun)
        # Fallthrough
        return (None, None)

    def parse(self, command):
        # Reset state; we may be reused.
        self.valid = False

        (verb, noun) = self.tokenise(command)
        if verb:
            self.__verb = verb
            self.valid = True
        else:
            self.__verb = None

        self.__noun = noun
    
    def __repr__(self):
        debug = "Parser object with: \n"
        debug += f"Verb: {self.__verb}\n"
        debug += f"Noun: {self.__noun}\n"
        debug += f"Valid: {self.valid}\n"
        return debug

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
