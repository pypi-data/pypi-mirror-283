
english_pronouns: dict[str, list[str]] = {
    "unspecified": [],
    "he": ["he", "him"],
    "she": ["she", "her"],
    "it": ["it", "its"],
    "they": ["they", "them"],
    "any": ["any"],
    "other": ["other"],
    "ask": ["ask"],
    "avoid": ["use name"],
}

german_pronouns: dict[str, list[str]] = {
    "unspecified": [],
    "he": ["Er", "Ihn"],
    "she": ["Sie", "Ihr"],
    "it": ["Es", "Seine"],
    "they": ["Neutral"],
    "any": ["Jede"],
    "other": ["Anderes"],
    "ask": ["Frag"],
    "avoid": ["Nutz Name"],
}
"""
Some translations like the "They/Them" are still in active debate about how to translate them, so dear developer:
Think about if the way this preset does it is good.
If it's good, just ignore this message.
If not, make your own.
"""
