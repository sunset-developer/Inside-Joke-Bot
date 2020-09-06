import string


def to_lower_without_punc(str):
    return str.lower().translate(str.maketrans('', '', string.punctuation))