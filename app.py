# Copyright (C) 2020  Aidan Stewart (sunset-developer)
import argparse
import os
import uuid
from configparser import ConfigParser
import pyfiglet
from discord.ext import commands
from tortoise import Tortoise
from core.cogs import JokeCog, UtilCog, GoofCog, AdminCog
from core.models import TriggeredMeme
from core.util import to_lower_without_punc, can_trigger_memes, can_execute_commands

config_file = 'config.ini'

config = ConfigParser()
bot = commands.Bot(help_command=None, command_prefix=None)


@bot.event
async def on_ready():
    print(pyfiglet.figlet_format('sunsetdev', 'graffiti'))
    print("Hi! I'm alive and ready to tell memes :)")


@bot.event
async def on_message(message):
    if not message.author.bot:
        if message.content[0] == bot.command_prefix and can_execute_commands(message.author, message.guild):
            await bot.process_commands(message)
        elif can_trigger_memes(message.author, message.guild):
            await meme_check(message)


@bot.event
async def on_guild_join(guild):
    for channel in guild.channels:
        try:
            welcome_msg = 'Thanks for inviting me! Learn my commands by using ' + bot.command_prefix + 'help'
            await channel.send(welcome_msg)
            return
        except:
            pass


async def meme_check(message):
    content = to_lower_without_punc(message.content)
    memes = await TriggeredMeme.filter(guild_did=message.guild.id, deleted=False)
    for meme in memes:
        if meme.trigger in content:
            if meme.nsfw and not message.channel.is_nsfw():
                return
            await message.channel.send(meme.meme)


async def db_init():
    username = config['DEFAULT']['dbusername']
    password = config['DEFAULT']['dbpassword']
    endpoint = config['DEFAULT']['dbendpoint']
    await Tortoise.init(db_url='mysql://{0}:{1}@{2}/{3}'.format(username, password, endpoint, 'comedibot'),
                        modules={"models": ['core.models']})
    await Tortoise.generate_schemas()


def init():
    config.read(config_file)
    bot.loop.create_task(db_init())
    bot.add_cog(AdminCog(bot))
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

        
if __name__ == '__main__':
    setup()
    init()
