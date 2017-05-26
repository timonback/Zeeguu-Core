from sqlalchemy.orm import relationship

from zeeguu.model.feed import db, RSSFeed
from zeeguu.model.user import User


class RSSFeedRegistration(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_bin'}
    __tablename__ = 'rss_feed_registration'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = relationship(User)

    rss_feed_id = db.Column(db.Integer, db.ForeignKey("rss_feed.id"))
    rss_feed = relationship(RSSFeed)

    def __init__(self, user, feed):
        self.user = user
        self.rss_feed = feed

    @classmethod
    def find_or_create(cls, user, feed):
        try:
            return (cls.query.filter(cls.user == user)
                    .filter(cls.rss_feed == feed)
                    .one())
        except sqlalchemy.orm.exc.NoResultFound:
            return cls(user, feed)

    @classmethod
    def feeds_for_user(cls, user):
        """
        would have been nicer to define a method on the User class get feeds,
        but that would pollute the user model, and it's not nice.
        :param user:
        :return:
        """
        return cls.query.filter(cls.user == user)

    @classmethod
    def with_id(cls, i):
        return (cls.query.filter(cls.id == i)).one()

    @classmethod
    def with_feed_id(cls, i, user):
        return (cls.query.filter(cls.rss_feed_id == i)) \
            .filter(cls.user_id == user.id).one()
