import csv
import os
import string

import aiofiles
from aiocsv import AsyncDictWriter, AsyncDictReader

from core.model import Joke, JokeNotFoundError

joke_cache = 'jokes.csv'
base_field_names = ['uid', 'parent_uid', 'date_created', 'deleted']
joke_field_names = base_field_names + ['author', 'author_did', 'trigger', 'joke', 'audio', 'nsfw']


async def cache_joke(joke):
    cache_existed = os.path.isfile(joke_cache)
    async with aiofiles.open(joke_cache, mode="a+", encoding="utf-8", newline="") as afp:
        writer = AsyncDictWriter(afp, joke_field_names, restval="None", delimiter=',', quoting=csv.QUOTE_MINIMAL)
        if not cache_existed:
            await writer.writeheader()
        await writer.writerow(joke.to_dict())


async def delete_joke(trigger, parent_uid, author_did):
    jokes = await get_jokes(parent_uid)
    async with aiofiles.open(joke_cache, mode="w", encoding="utf-8", newline="") as afp:
        writer = AsyncDictWriter(afp, joke_field_names, restval="None", delimiter=',', quoting=csv.QUOTE_MINIMAL)
        await writer.writeheader()
        for joke in jokes:
            if joke.author_did == author_did and joke.trigger == trigger:
                joke.deleted = True
                await writer.writerow(joke.to_dict())
                return joke


async def get_jokes(parent_uid):
    jokes = []
    if not os.path.isfile(joke_cache):
        raise JokeNotFoundError('Jokes cache not initialized, fix via submission.')
    async with aiofiles.open(joke_cache, mode="r", encoding="utf-8", newline="") as f:
        async for row in AsyncDictReader(f):
            if int(row['parent_uid']) == parent_uid and 'False' in row['deleted']:
                joke = Joke(int(row['parent_uid']), row['author'], int(row['author_did']), row['trigger'], row['joke'],
                            str(row['audio']), row['nsfw'])
                jokes.append(joke)
    if not jokes:
        raise JokeNotFoundError('No jokes were found with parent uid: ' + str(parent_uid))
    return jokes


async def filter_jokes_via_trigger(trigger, parent_uid):
    filtered_jokes = list(filter(lambda j: j.trigger in trigger.lower().translate(str.maketrans('', '', string.punctuation)) and
                         j.parent_uid == parent_uid, await get_jokes(parent_uid)))
    if not filtered_jokes:
        raise JokeNotFoundError('No jokes were found using trigger with parent uid: ' + str(parent_uid))
    return filtered_jokes
