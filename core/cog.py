import traceback

import aiofiles
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from tortoise.exceptions import OperationalError

from core.model import Joke, Goof
from core.util import to_lower_without_punc


class JokeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def submit(self, ctx, trigger_arg, joke_arg, audio_arg=None, nsfw=False):
        try:
            await Joke.create(guild_did=ctx.guild.id, author_did=ctx.author.id, joke=joke_arg, audio=audio_arg,
                              trigger=to_lower_without_punc(trigger_arg), nsfw=nsfw)
            await ctx.send(':white_check_mark: **Submitted :)**')
        except OperationalError:
            traceback.print_exc()
            await ctx.send(':x: **An error occurred, please try again :(**')

    @commands.command()
    async def submitnsfw(self, ctx, trigger_arg, joke_arg, audio_arg='None'):
        await self.submit(ctx, trigger_arg, joke_arg, audio_arg, True)

    @commands.command()
    async def delete(self, ctx, trigger_arg):
        jokes = await Joke.filter(trigger=to_lower_without_punc(trigger_arg), author_did=ctx.author.id,
                                  guild_did=ctx.guild.id, deleted=False).update(deleted=True)
        if not jokes:
            await ctx.send(':x: **I cant delete a joke you didn\'t tell :(**')
        else:
            await ctx.send(':white_check_mark: **Deleted :)**')

    @commands.command()
    async def get(self, ctx, trigger_arg):
        jokes = await Joke.filter(trigger=to_lower_without_punc(trigger_arg), guild_did=ctx.guild.id,
                                  deleted=False).all()
        if not jokes:
            await ctx.send(':x: **I cant find a joke that wasn\'t told :(**')
        else:
            joke_embed = discord.Embed(title='This joke has been told by:', color=discord.Color.dark_purple())
            for joke in jokes:
                joke_embed.add_field(name=ctx.guild.get_member(int(joke.author_did)), value=joke.joke)
            await ctx.send(embed=joke_embed)


class GoofCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def submitgoof(self, ctx, mention: discord.User, quote):
        try:
            await Goof.create(author_did=ctx.author.id, mention_did=mention.id, quote=quote, guild_did=ctx.guild.id)
            await ctx.send(':white_check_mark: **Submitted :)**')
        except OperationalError:
            traceback.print_exc()
            await ctx.send(':x: **An error occurred, please try again :(**')

    @commands.command()
    async def deletegoof(self, ctx, mention: discord.User, quote):
        goof = await Goof.filter(quote=quote, mention_did=mention.id, author_did=ctx.author.id,
                                 guild_did=ctx.guild.id, deleted=False).update(deleted=True)
        if not goof:
            await ctx.send(':x: **I cant delete a goof you didn\'t tell me about :(**')
        else:
            await ctx.send(':white_check_mark: **Deleted :)**')

    @commands.command()
    async def getgoof(self, ctx, mention: discord.User):
        goofs = await Goof.filter(guild_did=ctx.guild.id, mention_did=mention.id, deleted=False).all()
        if not goofs:
            await ctx.send(':x: **I cant find goofs that I don\'t know about :(**')
        else:
            goofs_embed = discord.Embed(title='Times ' + str(ctx.guild.get_member(mention.id)) + ' goofed:',
                                        color=discord.Color.dark_red())
            for goof in goofs:
                goofs_embed.add_field(value=goof.quote, name=goof.date_created.date())
            await ctx.send(embed=goofs_embed)


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @has_permissions(manage_messages=True)
    @commands.command()
    async def fdelete(self, ctx, trigger_arg):
        jokes = await Joke.filter(guild_did=ctx.guild.id, deleted=False, trigger=to_lower_without_punc(trigger_arg)) \
            .update(deleted=True)
        if not jokes:
            await ctx.send(':x: **I cant delete a joke that doesn\'t exist :(**')
        else:
            await ctx.send(':white_check_mark: **Deleted :)**')

    @has_permissions(manage_messages=True)
    @commands.command()
    async def fdeletegoof(self, ctx, mention: discord.User, quote):
        goof = await Goof.filter(quote=quote, mention_did=mention.id, guild_did=ctx.guild.id, deleted=False) \
            .update(deleted=True)
        if not goof:
            await ctx.send(':x: **I cant delete a goof that doesn\'t exist :(**')
        else:
            await ctx.send(':white_check_mark: **Deleted :)**')

    @has_permissions(manage_roles=True)
    @commands.command()
    async def genroles(self, ctx):
        await ctx.guild.create_role(name='comedian', color=discord.Color.dark_red())
        await ctx.guild.create_role(name='audience', color=discord.Color.dark_blue())
        await ctx.send(':white_check_mark: **Roles have been generated, please set permissions :)**')


class UtilCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def read_file(self, file):
        async with aiofiles.open('resources/' + file, mode="r") as f:
            return await f.read()

    @commands.command()
    async def help(self, ctx):
        await ctx.channel.send(await self.read_file('help.txt'))

    @commands.command()
    async def changes(self, ctx):
        await ctx.channel.send(await self.read_file('changes.txt'))

    @commands.command()
    async def stop(self, ctx):
        for client in self.bot.voice_clients:
            if client.channel is ctx.author.voice.channel:
                client.stop()

    @commands.command()
    async def leave(self, ctx):
        await self.stop(ctx)
        for client in self.bot.voice_clients:
            if client.channel is ctx.author.voice.channel:
                await client.disconnect()
