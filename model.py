import string
import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Boolean
from db.mysql import Base


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    uid = Column(String)
    parent_uid = Column(String)
    date_created = Column(Date)
    date_updated = Column(Date)
    active = Column(Boolean)

    def __init__(self, parent_uid):
        utcnow = datetime.utcnow()
        self.date_created = utcnow
        self.date_updated = utcnow
        self.uid = str(uuid.uuid4())
        self.parent_uid = parent_uid
        self.active = True


class Joke(BaseModel):
    __tablename__ = 'joke'
    author = Column(String)
    author_id = Column(String)
    trigger = Column(String)
    target = Column(String)
    joke = Column(String)

    def __init__(self, author, trigger, joke, target, parent_uid):
        super().__init__(parent_uid)
        self.trigger = trigger.translate(str.maketrans('', '', string.punctuation))
        self.joke = joke[:200]
        self.author = author.name
        self.author_id = author.id
        self.target = target.translate(str.maketrans('', '', string.punctuation)) if target is not None else None

    def __str__(self):
        return ">>> :triangular_flag_on_post: **Trigger**: `{0}`  \n" \
               ":fire: **Joke**: `{1}` \n" \
               ":pencil: **Author**: `{4}`\n" \
               ":alarm_clock: **Time (UTC)**: `{3}` \n" \
               ":desktop: **UID**: `{5}`" \
            .format(self.trigger, self.joke, self.uid, self.date_updated, self.author, self.uid)


class JokeNotFoundException(Exception):
    def __init__(self):
        exc_msg = ':x: **Joke not found or insufficient permission**'
        super(JokeNotFoundException, self).__init__(exc_msg)
