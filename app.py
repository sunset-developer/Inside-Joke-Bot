import random
import string

from discord.ext import commands

from cog import UserJokeCog, UtilCog
from config import TOKEN, COMMAND_PREFIX
from db.mysql import create_session
from model import Joke

bot = commands.Bot(command_prefix=COMMAND_PREFIX, help_command=None)


@bot.event
async def on_ready():
    print("bot initialized")


@bot.event
async def on_message(message):
    if message.author != bot.user:
        if not message.content[0] == COMMAND_PREFIX:
            await horny_check(message)
            await joke_check(message)
        else:
            await bot.process_commands(message)


async def joke_check(message):
    db_session = create_session()
    with db_session.begin():
        for joke in sorted(db_session.query(Joke).filter(Joke.active, Joke.parent_uid == message.guild.id).all(),
                           key=lambda j: len(j.trigger.split(' ')), reverse=True):
            if joke.trigger in message.content.lower().translate(str.maketrans('', '', string.punctuation)):
                if joke.target is None or joke.target == str(message.author.id):
                    await message.channel.send(joke.joke)
                    return


# Easter egg
async def horny_check(message):
    if 'horny' in message.content.lower():
        stds = ['Chancroid', 'Chlamydia', 'Crabs', 'Gonorrhea', 'Hepatitis',
                'Herpes', 'AIDS', 'Warts', 'HPV', 'Syphillis', 'Vaginal Yeast', 'Nothing']
        await message.channel.send('{0.author.name} smashed tf out of {1.name} and contracted *{2}*'
                                   .format(message, random.choice(message.guild.members), random.choice(stds)))


bot.add_cog(UtilCog(bot))
bot.add_cog(UserJokeCog(bot))
bot.run(TOKEN, bot=True)
