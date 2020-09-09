# Copyright (C) 2020  Aidan Stewart (sunset-developer)
import string
import discord


def to_lower_without_punc(str):
    return str.lower().translate(str.maketrans('', '', string.punctuation))


def can_execute_commands(user, guild):
    return _perm_check(user, guild, 'Comedian')


def can_trigger_memes(user, guild):
    return _perm_check(user, guild, 'Audience')


def _perm_check(user, guild, perm):
    can = False
    role = discord.utils.find(lambda r: r.name == perm, guild.roles)
    if role in user.roles or role is None:
        can = True
    return can
