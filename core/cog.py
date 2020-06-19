import os
import string
import traceback
from datetime import datetime

from discord import ClientException
from discord.ext import commands
from sqlalchemy import or_
from youtube_dl import DownloadError

from db.dbmodel import Joke
from db.mysql import Session
from core.model import JokeNotFoundException, YTDLSource


class JokeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _joke_clause(self, ctx, arg):
        parsed_arg = arg.translate(str.maketrans('', '', string.punctuation))
        get_any = or_(Joke.trigger == parsed_arg, Joke.uid == parsed_arg), Joke.active, Joke.parent_uid == ctx.guild.id
        get_permitted = get_any if ctx.message.author.guild_permissions.manage_messages else (
            get_any, Joke.author_id == ctx.author.id)
        return get_permitted, get_any

    def _get_joke(self, db_session, arg, ctx, requires_perm=False):
        permitted_joke, any_joke = self._joke_clause(ctx, arg)
        joke = db_session.query(Joke).filter(*permitted_joke if requires_perm else any_joke).first()
        if joke is None:
            raise JokeNotFoundException
        return joke


    @commands.command()
    async def submit(self, ctx, trigger_arg, joke_arg, audio=None):
        try:
            db_session = Session()
            with db_session.begin():
                try:
                    told_joke = self._get_joke(db_session, trigger_arg, ctx)
                    await ctx.send(':x: **this joke already exists, use the $update to edit this joke**\n'
                                   + str(told_joke))
                except JokeNotFoundException:
                    new_joke = Joke(ctx.message.author, trigger_arg.lower(), joke_arg, ctx.guild.id, audio)
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
            db_session = Session()
            with db_session.begin():
                self._get_joke(db_session, arg, ctx, True).active = False
                await ctx.send(':white_check_mark: **Deleted**')
        except JokeNotFoundException as e:
            await ctx.send(str(e))
        except Exception:
            exc = traceback.format_exc()
            print(exc)
            await ctx.send(':x: Fatal Error:\n ' + exc)

    @commands.command()
    async def update(self, ctx, trigger_arg, joke_arg, audio=None):
        try:
            db_session = Session()
            with db_session.begin():
                joke = self._get_joke(db_session, trigger_arg, ctx, True)
                joke.joke = joke_arg
                if audio is not None:
                    joke.audio = audio
                joke.date_updated = datetime.utcnow()
                await ctx.send(':white_check_mark: **Updated**')
        except JokeNotFoundException as e:
            await ctx.send(str(e))
        except Exception:
            exc = traceback.format_exc()
            print(exc)
            await ctx.send(':x: Fatal Error:\n ' + exc)

    @commands.command()
    async def get(self, ctx, trigger_arg):
        try:
            db_session = Session()
            with db_session.begin():
                await ctx.send(str(self._get_joke(db_session, trigger_arg, ctx)))
        except JokeNotFoundException as e:
            await ctx.send(str(e))
        except Exception:
            exc = traceback.format_exc()
            print(exc)
            await ctx.send(':x: Fatal Error:\n ' + exc)


    @commands.command()
    async def stop(self, ctx):
        for client in self.bot.voice_clients:
            if client.channel is ctx.author.voice.channel:
                client.stop()


    @commands.command()
    async def leave(self, ctx):
        for client in self.bot.voice_clients:
            if client.channel is ctx.author.voice.channel:
            await client.disconnect()


class UtilCog(commands.Cog):
    @commands.command()
    async def help(self, ctx):
        await self.read_file(ctx, 'resources/help.txt')

    @commands.command()
    async def changes(self, ctx):
        await self.read_file(ctx, 'resources/changes.txt')

    async def read_file(self, ctx, file):
        with open(file, 'r') as help:
            await ctx.channel.send(help.read())
