import traceback

import aiofiles
import discord
from discord.ext import commands

from core import cache
from core.model import Joke, JokeNotFoundError


class JokeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def submit(self, ctx, trigger_arg, joke_arg, audio_arg='None', nsfw=False):
        joke = Joke(ctx.guild.id, ctx.author.name, ctx.author.id, trigger_arg, joke_arg, audio_arg, nsfw)
        await cache.cache_joke(joke)
        await ctx.send(':white_check_mark: **Submitted :)**')

    @commands.command()
    async def submitnsfw(self, ctx, trigger_arg, joke_arg, audio_arg='None'):
        await self.submit(ctx, trigger_arg, joke_arg, audio_arg, True)

    @commands.command()
    async def delete(self, ctx, trigger_arg):
        try:
            deleted_joke = await cache.delete_joke(trigger_arg, ctx.guild.id, ctx.author.id)
            await ctx.send(':white_check_mark: **Deleted :)**', embed=deleted_joke.to_embed())
        except JokeNotFoundError:
            await ctx.send(':x: **Your joke(s) could not be found and therefore not deleted :(**')

    @commands.command()
    async def get(self, ctx, trigger_arg):
        try:
            jokes = await cache.filter_jokes_via_trigger(trigger_arg, ctx.guild.id)
            for joke in jokes:
                await ctx.send(embed=joke.to_embed())
        except JokeNotFoundError:
            await ctx.send(':x: **Could not find the joke you were looking for :(**')

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
    async def read_file(self, file):
        async with aiofiles.open('resources/' + file, mode="r") as f:
            return await f.read()

    @commands.command()
    async def help(self, ctx):
        await ctx.channel.send(await self.read_file('help.txt'))

    @commands.command()
    async def changes(self, ctx):
        await ctx.channel.send(await self.read_file('changes.txt'))
