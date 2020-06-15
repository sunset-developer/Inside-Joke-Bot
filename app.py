import random
import string

from discord.ext import commands
from db.dbmodel import Joke
from db.mysql import create_session
from core.cog import JokeCog, UtilCog
from core.config import TOKEN, COMMAND_PREFIX

bot = commands.Bot(command_prefix=COMMAND_PREFIX, help_command=None)
joke_cog = JokeCog(bot)


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
        jokes = db_session.query(Joke).filter(Joke.active, Joke.parent_uid == message.guild.id).all()
        for joke in sorted(jokes, key=lambda j: len(j.trigger.split(' ')), reverse=True):
            if joke.trigger in message.content.lower().translate(str.maketrans('', '', string.punctuation)):
                await message.channel.send(joke.joke)
                if joke.audio is not None:
                    await joke_cog.play(joke, message.author.voice.channel)


# Easter egg
async def horny_check(message):
    if 'horny' in message.content.lower():
        stds = ['Chancroid', 'Chlamydia', 'Crabs', 'Gonorrhea', 'Hepatitis',
                'Herpes', 'AIDS', 'Warts', 'HPV', 'Syphillis', 'Vaginal Yeast', 'Nothing']
        await message.channel.send('{0.author.name} smashed tf out of {1.name} and contracted *{2}*'
                                   .format(message, random.choice(message.guild.members), random.choice(stds)))


bot.add_cog(UtilCog(bot))
bot.add_cog(joke_cog)
bot.run(TOKEN, bot=True)
