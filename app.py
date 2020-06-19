import asyncio
import os
import random
import string
import time

from discord import ClientException
from discord.ext import commands

from core.model import YTDLSource
from db.dbmodel import Joke
from db.mysql import Session
from core.cog import JokeCog, UtilCog
from core.config import TOKEN, COMMAND_PREFIX

bot = commands.Bot(command_prefix=COMMAND_PREFIX, help_command=None)


@bot.event
async def on_ready():
    print("bot initialized")


@bot.event
async def on_message(message):
    if message.author != bot.user:
        if not message.content[0] == COMMAND_PREFIX:
            await joke_check(message)
            await card_check(message)
            await horny_check(message)
        else:
            await bot.process_commands(message)


async def joke_check(message):
    db_session = Session()
    with db_session.begin():
        jokes = db_session.query(Joke).filter(Joke.active, Joke.parent_uid == message.guild.id).all()
        for joke in sorted(jokes, key=lambda j: len(j.trigger.split(' ')), reverse=True):
            if joke.trigger in message.content.lower().translate(str.maketrans('', '', string.punctuation)):
                await message.channel.send(joke.joke)
                if message.author.voice is not None and joke.audio is not None:
                    await play_joke_audio(joke, message.author.voice)
                return


async def play_joke_audio(joke, channel):
    try:
        await channel.connect()
    except ClientException:
        pass
    for client in bot.voice_clients:
        if client.channel is channel:
            filename, player = await YTDLSource.from_url(joke.audio)
            client.play(player, after=lambda e: os.remove(filename))


async def disconnect_from_voice_when_idle():
    await bot.wait_until_ready()
    while True:
        for client in bot.voice_clients:
            if len(client.channel.members) == 1:
                await client.disconnect()
        await asyncio.sleep(3600)


# Easter egg
async def horny_check(message):
    if 'horny' in message.content.lower():
        stds = ['Chancroid', 'Chlamydia', 'Crabs', 'Gonorrhea', 'Hepatitis',
                'Herpes', 'AIDS', 'Warts', 'HPV', 'Syphillis', 'Vaginal Yeast', 'Nothing']
        await message.channel.send('{0.author.name} smashed tf out of {1.name} and contracted *{2}*'
                                   .format(message, random.choice(message.guild.members), random.choice(stds)))


# Easter egg
async def card_check(message):
    if 'card' in message.content.lower():
        await message.channel.send('https://allbad.cards/')


bot.loop.create_task(disconnect_from_voice_when_idle())
bot.add_cog(UtilCog(bot))
bot.add_cog(JokeCog(bot))
bot.run(TOKEN, bot=True)
