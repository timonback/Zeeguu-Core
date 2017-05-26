import datetime

import zeeguu

from zeeguu.model.bookmark import Bookmark

db = zeeguu.db


class BookmarkPriorityARTS(db.Model):
    __tablename__ = 'bookmark_priority_arts'
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    bookmark_id = db.Column(db.Integer, db.ForeignKey('bookmark.id'), primary_key=True)
    bookmark = db.relationship(Bookmark)

    priority = db.Column(db.Float)

    updated = db.Column(db.DateTime, server_default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    def __init__(self, bookmark, priority):
        self.bookmark = bookmark
        self.priority = priority
