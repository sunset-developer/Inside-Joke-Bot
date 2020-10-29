# Copyright (C) 2020  Aidan Stewart (sunset-developer)
import uuid

from tortoise import fields
from tortoise.models import Model


class BaseModel(Model):
    id = fields.IntField(pk=True)
    uid = fields.UUIDField(max_length=36, default=uuid.uuid4)
    date_created = fields.DatetimeField(auto_now_add=True)
    guild_did = fields.CharField(max_length=18, null=True)
    author_did = fields.CharField(max_length=18, null=True)
    deleted = fields.BooleanField(default=False)

    class Meta:
        abstract = True


class Goof(BaseModel):
    mention_did = fields.CharField(max_length=18, null=True)
    quote = fields.CharField(max_length=255)

    class Meta:
        table = 'goof'


class TriggeredMeme(BaseModel):
    trigger = fields.CharField(max_length=255)
    meme = fields.CharField(max_length=255)
    nsfw = fields.BooleanField(default=False)

    class Meta:
        table = 'meme'