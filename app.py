import asyncio
import os
import string
from configparser import ConfigParser, NoOptionError

import pyfiglet as pyfiglet
from discord import ClientException, LoginFailure
from discord.ext import commands

from core.cache import get_jokes, filter_jokes_via_trigger
from core.cog import JokeCog, UtilCog
from core.model import YTDLSource

config = ConfigParser()
bot = commands.Bot(help_command=None, command_prefix=None)


@bot.event
async def on_ready():
    print(pyfiglet.figlet_format('sunsetdev', 'graffiti'))
    print("I'm aliiiiive!")


@bot.event
async def on_message(message):
    if message.author != bot.user:
        if message.content[0] == bot.command_prefix:
            await bot.process_commands(message)
        else:
            await joke_check(message)


@bot.event
async def on_guild_join(guild):
    for channel in guild.channels:
        try:
            welcome_msg = 'Thanks for inviting me! To start, learn my commands by using ' + bot.command_prefix + 'help'
            await channel.send(welcome_msg)
            return
        except:
            pass


async def joke_check(message):
    jokes = await filter_jokes_via_trigger(message.content, message.guild.id)
    for joke in sorted(jokes, key=lambda j: len(j.trigger.split(' ')), reverse=True):
        if joke.nsfw and not message.channel.is_nsfw():
            return
        await message.channel.send(joke.joke)
        if message.author.voice is not None and joke.audio is not None:
            await play_joke_audio(joke, message.author.voice.channel)
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


async def disconnect_from_voice_when_alone():
    await bot.wait_until_ready()
    while True:
        for client in bot.voice_clients:
            if len(client.channel.members) == 1:
                await client.disconnect()
        await asyncio.sleep(3600)


def setup():
    if config.has_section('DEFAULT'):
        config.add_section('DEFAULT')
    config.set('DEFAULT', 'cmdpfx', input('Input command prefix then press enter: '))
    config.set('DEFAULT', 'token', input('Input token then press enter: '))
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    init()


def init():
    config_file = 'config.ini'
    try:
        config.read(config_file)
        bot.command_prefix = config.get('DEFAULT', 'cmdpfx')
        bot.run(config.get('DEFAULT', 'token'), bot=True)
    except NoOptionError:
        setup()
    except LoginFailure:
        os.remove(config_file)


bot.loop.create_task(disconnect_from_voice_when_alone())
bot.add_cog(UtilCog(bot))
bot.add_cog(JokeCog(bot))
init()
