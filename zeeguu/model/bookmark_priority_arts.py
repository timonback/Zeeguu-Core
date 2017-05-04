import zeeguu

db = zeeguu.db


class BookmarkPriorityARTS(db.Model):
    __tablename__ = 'bookmark_priority_arts'
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    id = db.Column(db.Integer, primary_key=True)
    bookmark_id = db.Column(db.Integer, db.ForeignKey('bookmark.id'))

    priority = db.Column(db.Float)

    updated = db.Column(db.DateTime)
