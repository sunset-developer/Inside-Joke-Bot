import argparse
import asyncio
import os
import pyfiglet
from configparser import ConfigParser
from discord import ClientException
from discord.ext import commands
from tortoise import Tortoise
from core.cog import JokeCog, UtilCog, GoofCog
from core.model import YTDLSource, Joke
from core.util import to_lower_without_punc, can_trigger_jokes, can_execute_commands

config_file = 'config.ini'
arg = argparse.ArgumentParser(description='Comedibot Configuration')
config = ConfigParser()
bot = commands.Bot(help_command=None, command_prefix=None)


@bot.event
async def on_ready():
    print(pyfiglet.figlet_format('sunsetdev', 'graffiti'))
    print("Hi! I'm alive and ready to tell jokes :)")


@bot.event
async def on_disconnect():
    await Tortoise.close_connections()


@bot.event
async def on_message(message):
    if message.author != bot.user:
        if message.content[0] == bot.command_prefix and can_execute_commands(message.author, message.guild):
            await bot.process_commands(message)
        elif can_trigger_jokes(message.author, message.guild):
            await joke_check(message)


@bot.event
async def on_guild_join(guild):
    for channel in guild.channels:
        try:
            welcome_msg = 'Thanks for inviting me! Learn my commands by using ' + bot.command_prefix + 'help'
            await channel.send(welcome_msg)
            return
        except:
            pass


async def joke_check(message):
    content = to_lower_without_punc(message.content)
    jokes = await Joke.filter(parent_uid=message.guild.id, deleted=False).all()
    for joke in jokes:
        if joke.trigger in content:
            if joke.nsfw and not message.channel.is_nsfw():
                return
            await message.channel.send(joke.joke)
            if message.author.voice is not None and joke.audio is not None:
                await play_joke_audio(joke, message.author.voice.channel)


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


async def db_init():
    username = config['DEFAULT']['dbusername']
    password = config['DEFAULT']['dbpassword']
    endpoint = config['DEFAULT']['dbendpoint']
    await Tortoise.init(db_url='mysql://{0}:{1}@{2}/{3}'.format(username, password, endpoint, 'comedibot'),
                        modules={"models": ['core.model']})
    await Tortoise.generate_schemas()


def init():
    config.read(config_file)
    bot.loop.create_task(db_init())
    bot.loop.create_task(disconnect_from_voice_when_alone())
    bot.add_cog(UtilCog(bot))
    bot.add_cog(JokeCog(bot))
    bot.add_cog(GoofCog(bot))
    bot.command_prefix = config['DEFAULT']['prefix']
    bot.run(config['DEFAULT']['token'], bot=True)


def set_config(args):
    if config.has_section('DEFAULT'):
        config.add_section('DEFAULT')
    config.set('DEFAULT', 'prefix', args.prefix)
    config.set('DEFAULT', 'token', args.token)
    config.set('DEFAULT', 'dbusername', args.dbusername)
    config.set('DEFAULT', 'dbpassword', args.dbpassword)
    config.set('DEFAULT', 'dbendpoint', args.dbendpoint)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def update_config(args):
    config.read(config_file)
    if args.prefix:
        config['DEFAULT']['prefix'] = args.prefix
    if args.token:
        config['DEFAULT']['token'] = args.token
    if args.dbusername:
        config['DEFAULT']['dbusername'] = args.dbusername
    if args.dbpassword:
        config['DEFAULT']['dbpassword'] = args.dbpassword
    if args.dbendpoint:
        config['DEFAULT']['dbendpoint'] = args.dbendpoint
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def add_args():
    arg.add_argument("-pfx", "--prefix")
    arg.add_argument("-tkn", "--token")
    arg.add_argument("-dbu", "--dbusername")
    arg.add_argument("-dbp", "--dbpassword")
    arg.add_argument("-dbe", "--dbendpoint")


def setup():
    add_args()
    args = arg.parse_args()
    if os.path.exists(config_file):
        update_config(args)
    else:
        set_config(args)


setup()
init()
