import a2bw

FORM = 0
DIACRITICS = 1
GLOSS = 2

"""
This contains a lot of very arbitrary decisions, many of which may introduce
errors (e.g. if any of the characters are already in a2bwtable.

Allan, 26/07/2017
"""

"""
Added "U":"u" to allow for LDC dict
"""

HTKDICT = {"$":"X", "*":"V", "|":"QA", "}":"Q", "'":"Q", "`":"A", "U":"u"}

def HTKFriendly(text0):
    """
    Some characters just plain confuse the HTK
    """
    """
    Run all sorts of variations, esp including/excluding case-markers

    (i) excluding case-markers is a good thing
    (ii) simple-minded treatment of shaddas is a bad thing. We haven't found
    a clever thing that is better than just ignoring them
    """
    if isinstance(text0, list):
        return map(HTKFriendly, text0)
    else:
        text0 = a2bw.old2new(text0)
        for c in HTKDICT:
            text0 = text0.replace(c, HTKDICT[c])
        return text0
