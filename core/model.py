import asyncio
import string
import uuid
from datetime import datetime

import discord
import youtube_dl


class BaseModel:
    def __init__(self, parent_uid=None, date_created=datetime.utcnow(), uid=str(uuid.uuid4()), deleted=False):
        self.date_created = date_created
        self.uid = uid
        self.parent_uid = parent_uid
        self.deleted = deleted

    def to_dict(self):
        return {
            'uid': self.uid,
            'parent_uid': self.parent_uid,
            'date_created': self.date_created,
            'deleted': self.deleted
        }


class Joke(BaseModel):

    def __init__(self, parent_uid, author, author_did, trigger, joke, audio, nsfw):
        super(Joke, self).__init__(parent_uid)
        self.trigger = trigger.translate(str.maketrans('', '', string.punctuation))
        self.joke = joke
        self.author = author
        self.author_did = author_did
        self.audio = audio
        self.nsfw = nsfw

    def to_dict(self):
        return dict(super().to_dict(), **{
            'author_did': self.author_did,
            'author': self.author,
            'trigger': self.trigger,
            'joke': self.joke,
            'audio': self.audio,
            'nsfw': self.nsfw
        })

    def to_embed(self):
        joke_embed = discord.Embed(title=self.author + '\'s Joke', color=discord.Color.dark_purple())
        joke_embed.add_field(name='Trigger', value=self.trigger, inline=False)
        joke_embed.add_field(name='Joke', value=self.joke, inline=False)
        joke_embed.add_field(name='Audio', value=self.audio, inline=False)
        joke_embed.add_field(name='Nsfw', value=str(self.nsfw), inline=False)
        return joke_embed

    def __str__(self):
        return ":triangular_flag_on_post: **Trigger**: `{0}`  \n" \
               ":fire: **Joke**: {1}\n" \
               ":pencil: **Author**: {2}\n" \
               ":alarm_clock: **Time (UTC)**: {3}\n" \
               ":speaker: **Audio**: {4}" \
            .format(self.trigger, self.joke, self.author, self.date_created, self.audio)





class JokeNotFoundError(Exception):
    def __init__(self, message):
        super(JokeNotFoundError, self).__init__(message)


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
