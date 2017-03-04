#
import random
from sqlalchemy import Column, Table, ForeignKey, Integer
import sqlalchemy.orm
from sqlalchemy.orm import relationship


from zeeguu import util
from zeeguu.model.language import Language
import datetime
import json

import zeeguu

db = zeeguu.db

from zeeguu.model.user_word import UserWord

starred_words_association_table = Table('starred_words_association', db.Model.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('starred_word_id', Integer, ForeignKey('user_word.id'))
)

class User(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    password = db.Column(db.LargeBinary(255))
    password_salt = db.Column(db.LargeBinary(255))
    learned_language_id = db.Column(
        db.String(2),
        db.ForeignKey("language.id")
    )
    learned_language = sqlalchemy.orm.relationship("Language", foreign_keys=[learned_language_id])
    starred_words = relationship("UserWord", secondary="starred_words_association")

    native_language_id = db.Column(
        db.String (2),
        db.ForeignKey("language.id")
    )
    native_language = sqlalchemy.orm.relationship("Language", foreign_keys=[native_language_id])

    def __init__(self, email, username, password, learned_language=None, native_language = None):
        self.email = email
        self.name = username
        self.update_password(password)
        self.learned_language = learned_language or Language.default_learned()
        self.native_language = native_language or Language.default_native_language()

    def __repr__(self):
        return '<User %r>' % (self.email)

    def has_starred(self,word):
        return word in self.starred_words

    def star(self, word):
        self.starred_words.append(word)

    def details_as_dictionary(self):
        return dict (
            email=self.email,
            name=self.name,
            learned_language=self.learned_language_id,
            native_language=self.native_language_id
        )

    def set_learned_language(self, code):
        self.learned_language = Language.find(code)

    def set_native_language(self, code):
        self.native_language = Language.find(code)

    @sqlalchemy.orm.validates("email")
    def validate_email(self, col, email):
        if "@" not in email:
            raise ValueError("Invalid email address")
        return email

    @sqlalchemy.orm.validates("password")
    def validate_password(self, col, password):
        if password is None or len(password) == 0:
            raise ValueError("Invalid password")
        return password

    @sqlalchemy.orm.validates("name")
    def validate_name(self, col, name):
        if name is None or len(name) == 0:
            raise ValueError("Invalid username")
        return name

    def update_password(self, password):
        self.password_salt = "".join(
            chr(random.randint(0, 255)) for i in range(32)
        )
        self.password = util.password_hash(password, self.password_salt)

    def all_bookmarks(self, after_date=datetime.datetime(1970,1,1), before_date=datetime.date.today() + datetime.timedelta(days=1)):
        from zeeguu.model.bookmark import Bookmark
        return Bookmark.query.\
            filter_by(user_id=self.id).\
            filter(Bookmark.time >= after_date). \
            filter(Bookmark.time <= before_date). \
            order_by(Bookmark.time.desc()).all()

    def bookmarks_chronologically(self):
        from zeeguu.model.bookmark import Bookmark
        return Bookmark.query.filter_by(user_id=self.id).order_by(Bookmark.time.desc()).all()

    def bookmarks_by_date(self, after_date=datetime.datetime(1970,1,1)):
        """

        :param after_date:
        :return: a pair of 1. a dict with date-> bookmarks and 2. a sorted list of dates
        """
        def extract_day_from_date(bookmark):
            return (bookmark, bookmark.time.replace(bookmark.time.year, bookmark.time.month, bookmark.time.day,0,0,0,0))

        bookmarks = self.all_bookmarks(after_date)
        bookmarks_by_date = dict()

        for elem in map(extract_day_from_date, bookmarks):
            bookmarks_by_date.setdefault(elem[1],[]).append(elem[0])

        sorted_dates = bookmarks_by_date.keys()
        sorted_dates.sort(reverse=True)
        return bookmarks_by_date, sorted_dates

    def bookmarks_by_day(self, with_context, after_date=datetime.datetime(2010,1,1)):
        bookmarks_by_date, sorted_dates = self.bookmarks_by_date(after_date)

        dates = []
        for date in sorted_dates:
            bookmarks = []
            for bookmark in bookmarks_by_date[date]:
                bookmarks.append(bookmark.json_serializable_dict(with_context))
            date_entry = dict(
                date=date.strftime("%A, %d %B %Y"),
                bookmarks=bookmarks
            )
            dates.append(date_entry)
        return dates

    def bookmarks_to_study(self, bookmark_count):
        from zeeguu.model.bookmark import Bookmark
        from zeeguu.model.ranked_word import RankedWord

        all_bookmarks_query = Bookmark.query.\
            filter_by(user_id=self.id).\
            join(UserWord).\
            join(RankedWord).\
            filter(UserWord.id == Bookmark.origin_id).\
            filter(UserWord.rank_id == RankedWord.id).\
            order_by(RankedWord.rank.asc())
        all_bookmarks = all_bookmarks_query.all()

        good_for_study=[]
        size = 0
        for b in all_bookmarks:
            if b.good_for_study():
                good_for_study.append(b)
                size += 1

            if size == bookmark_count:
                break

        if size < bookmark_count:
        # we did not find enough words to study which are ranked
        # add all the non-ranked ones, in chronological order

            all_bookmarks = Bookmark.query. \
                filter_by(user_id=self.id). \
                join(UserWord). \
                filter(UserWord.id == Bookmark.origin_id). \
                filter(UserWord.rank_id == None). \
                order_by(Bookmark.time.desc()).all()

            for b in all_bookmarks:
                if b.good_for_study():
                    good_for_study.append(b)
                    size += 1

                if size == bookmark_count:
                    break

        return map(lambda x: x.json_serializable_dict(), good_for_study)


    # returns array with added bookmark amount per each date for the last year
    # this function is for the activity_graph, generates data
    def bookmark_counts_by_date(self):

        # compute bookmark_counts_by_date
        year = datetime.date.today().year - 1  # get data from year 2015(if this year is 2016)
        month = datetime.date.today().month
        bookmarks_dict, dates = self.bookmarks_by_date(datetime.datetime(year, month, 1))

        counts = []
        for date in dates:
            the_date = date.strftime('%Y-%m-%d')
            the_count = len(bookmarks_dict[date])
            counts.append(dict(date=the_date, count=the_count))

        bookmark_counts_by_date = json.dumps(counts)
        return bookmark_counts_by_date

    # returns array with learned and learning words count per each month for the last year
    # this function is for the line_graph, generates data
    def learner_stats_data(self):

        # compute learner_stats_data
        from zeeguu.model.learner_stats.learner_stats import compute_learner_stats
        learner_stats_data = compute_learner_stats(self)

        return learner_stats_data

    def user_words(self):
        return map((lambda x: x.origin.word), self.all_bookmarks())

    def bookmark_count(self):
        return len(self.all_bookmarks())

    def word_count(self):
        return len(self.user_words())

    @classmethod
    def find_all(cls):
        return User.query.all()

    @classmethod
    def find(cls, email):
        return User.query.filter(User.email == email).one()

    @classmethod
    def find_by_id(cls, id):
        return User.query.filter(User.id == id).one()

    @classmethod
    def authorize(cls, email, password):
        try:
            user = cls.query.filter(cls.email == email).one()
            if user.password == util.password_hash(password,
                                                   user.password_salt):
                return user
        except sqlalchemy.orm.exc.NoResultFound:
            return None