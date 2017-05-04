import zeeguu
from sqlalchemy.sql import func

db = zeeguu.db


class BookmarkPriorityARTS(db.Model):
    __tablename__ = 'bookmark_priority_arts'
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    id = db.Column(db.Integer, primary_key=True)
    bookmark_id = db.Column(db.Integer, db.ForeignKey('bookmark.id'))

    priority = db.Column(db.Float)

    updated = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def __init__(self, bookmark_id, priority):
        self.bookmark_id = bookmark_id
        self.priority = priority
