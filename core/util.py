import string


def to_lower_without_punc(str):
    return str.lower().translate(str.maketrans('', '', string.punctuation))

def can_submit(author, guild):
    for role in guild.roles:
        if role.name == 'Comedian':
            if author.role:
                pass



