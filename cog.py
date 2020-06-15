import string
import traceback
from datetime import datetime

from discord.ext import commands
from sqlalchemy import or_

from db.mysql import create_session
from model import Joke, JokeNotFoundException


def _encode(text):
    return text.encode('ascii', 'ignore').decode('ascii')


class UserJokeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    def _get_joke(self, db_session, arg, ctx, requires_perm=False):
        parsed_arg = arg.translate(str.maketrans('', '', string.punctuation))
        joke_clause = or_(Joke.trigger == parsed_arg,
                          Joke.uid == parsed_arg), Joke.active, Joke.parent_uid == ctx.guild.id
        if ctx.message.author.guild_permissions.manage_messages or not requires_perm:
            joke = db_session.query(Joke).filter(*joke_clause).first()
        else:
            joke = db_session.query(Joke).filter(*joke_clause, Joke.author_id == ctx.author.id).first()
        if joke is None:
            raise JokeNotFoundException
        return joke

    @commands.command()
    async def submit(self, ctx, trigger_arg, joke_arg, target_arg=None):
        try:
            db_session = create_session()
            with db_session.begin():
                try:
                    told_joke = self._get_joke(db_session, trigger_arg, ctx)
                    await ctx.send(':x: **this joke already exists, use $append or $update to edit this joke**\n'
                                   + str(told_joke))
                except JokeNotFoundException:
                    new_joke = Joke(ctx.message.author, trigger_arg.lower(), joke_arg, target_arg, ctx.guild.id)
                    if new_joke.trigger:
                        db_session.add(new_joke)
                        await ctx.send(':white_check_mark: **Submitted**')
                    else:
                        await ctx.send(':x: **Illegal trigger**')
        except Exception:
            exc = traceback.format_exc()
            print(exc)
            await ctx.send(':x: Fatal Error:\n ' + exc)

    @commands.command()
    async def delete(self, ctx, arg):
        try:
            db_session = create_session()
            with db_session.begin():
                joke = self._get_joke(db_session, arg, ctx, True)
                joke.active = False
                await ctx.send(':white_check_mark: **Deleted**')
        except JokeNotFoundException as e:
            await ctx.send(str(e))
        except Exception:
            exc = traceback.format_exc()
            print(exc)
            await ctx.send(':x: Fatal Error:\n ' + exc)

    @commands.command()
    async def append(self, ctx, trigger_arg, joke_arg):
        try:
            db_session = create_session()
            with db_session.begin():
                joke = self._get_joke(db_session, trigger_arg, ctx, True)
                joke.joke = joke.joke + ' ' + joke_arg
                joke.on_update()
                await ctx.send(':white_check_mark: **Appended**')
        except JokeNotFoundException as e:
            await ctx.send(str(e))
        except Exception:
            exc = traceback.format_exc()
            print(exc)
            await ctx.send(':x: Fatal Error:\n ' + exc)

    @commands.command()
    async def update(self, ctx, trigger_arg, joke_arg, target_arg=None):
        try:
            db_session = create_session()
            with db_session.begin():
                joke = self._get_joke(db_session, trigger_arg, ctx, True)
                joke.joke = joke_arg
                joke.target = target_arg
                joke.date_updated = datetime.utcnow()
                await ctx.send(':white_check_mark: **Updated**')
        except JokeNotFoundException as e:
            await ctx.send(str(e))
        except Exception:
            exc = traceback.format_exc()
            print(exc)
            await ctx.send(':x: Fatal Error:\n ' + exc)

    @commands.command()
    async def get(self, ctx, arg):
        try:
            db_session = create_session()
            with db_session.begin():
                joke = self._get_joke(db_session, arg, ctx)
                await ctx.send(str(joke))
        except JokeNotFoundException as e:
            await ctx.send(str(e))
        except Exception:
            exc = traceback.format_exc()
            print(exc)
            await ctx.send(':x: Fatal Error:\n ' + exc)


async def read_file(ctx, file):
    with open(file, 'r') as help:
        await ctx.channel.send(help.read())


class UtilCog(commands.Cog):
    @commands.command()
    async def help(self, ctx):
        await read_file(ctx, 'help.txt')

    @commands.command()
    async def changes(self, ctx):
        await read_file(ctx, 'changes.txt')
