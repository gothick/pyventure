# Adapted from https://stackoverflow.com/a/38982008/300836
def commalist(items):
    if items:
        start, last = items[:-1], items[-1]

        if start:
            return "{} and {}".format(", ".join(start), last)
        else:
            return last
    return ""
