import zeeguu
from sqlalchemy import Column, UniqueConstraint, Integer, ForeignKey, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from zeeguu.model import Url, User
from zeeguu.model.language import Language


class Article(zeeguu.db.Model):
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    id = Column(Integer, primary_key=True)

    url_id = Column(Integer, ForeignKey(Url.id))
    url = relationship(Url)

    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship(User)

    title = Column(String(255))

    language_id = Column(String(2), ForeignKey(Language.id))
    language = relationship(Language)

    # Good to cache this somewhere
    estimated_difficulty = Column(Integer)

    # Useful for ordering past read articles
    last_accessed = Column(DateTime)

    # User Interactions
    opened = Column(Boolean)
    reading_time = Column(Integer)

    # User annotations
    starred = Column(Boolean)

    # User feedback
    liked = Column(Boolean)
    disliked = Column(Boolean)
    too_easy = Column(Boolean)
    too_hard = Column(Boolean)

    # Together an url_id and user_id identify an article
    UniqueConstraint(url_id, user_id)

    def __init__(self, _title, url, language, last_accessed, user, liked):
        pass


