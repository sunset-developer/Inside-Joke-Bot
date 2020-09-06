import asyncio
import uuid

import discord
import youtube_dl
from tortoise import fields
from tortoise.models import Model


class BaseModel(Model):
    id = fields.IntField(pk=True)
    uid = fields.TextField(default=str(uuid.uuid4()))
    date_created = fields.DatetimeField(auto_now_add=True)
    parent_uid = fields.TextField(null=True)
    deleted = fields.BooleanField(default=False)

    class Meta:
        abstract = True


class Goof(BaseModel):
    author_did = fields.TextField()
    mention_did = fields.TextField()
    mention_name = fields.TextField()
    quote = fields.TextField()

    class Meta:
        table = 'goof'


class Joke(BaseModel):
    author = fields.TextField()
    author_did = fields.TextField()
    trigger = fields.TextField()
    joke = fields.TextField()
    audio = fields.TextField(null=True)
    nsfw = fields.BooleanField(default=False)

    class Meta:
        table = 'joke'

    def to_embed(self):
        joke_embed = discord.Embed(title=self.author + '\'s Joke', color=discord.Color.dark_purple())
        joke_embed.add_field(name='Trigger', value=self.trigger, inline=False)
        joke_embed.add_field(name='Joke', value=self.joke, inline=False)
        joke_embed.add_field(name='Audio', value=self.audio, inline=False)
        joke_embed.add_field(name='Nsfw', value=str(self.nsfw), inline=False)
        return joke_embed




youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return filename, cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
