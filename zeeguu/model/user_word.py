from datetime import time

import sqlalchemy.orm
from sqlalchemy.orm.exc import NoResultFound
from wordstats import Word

import zeeguu
from zeeguu import util

db = zeeguu.db

from zeeguu.model.language import Language


class UserWord(db.Model, util.JSONSerializable):
    __tablename__ = 'user_word'
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(255), nullable=False)
    language_id = db.Column(db.String(2), db.ForeignKey(Language.id))
    language = db.relationship(Language)
    db.UniqueConstraint(word, language_id)

    IMPORTANCE_LEVEL_STEP = 1000
    IMPOSSIBLE_RANK = 1000000
    IMPOSSIBLE_IMPORTANCE_LEVEL = IMPOSSIBLE_RANK / IMPORTANCE_LEVEL_STEP

    def __init__(self, word, language):
        self.word = word
        self.language = language

    def __repr__(self):
        return '<UserWord %r>' % (self.word)

    def serialize(self):
        return self.word

    # returns a number between 0 and 10
    def importance_level(self):
        stats = Word.stats(self.word, self.language.id)
        if stats:
            return int(min(stats.importance, 10))
        else:
            return 0

    # we use this in the bookmarks.html to show the importance of a word
    def importance_level_string(self):
        b = "|"
        return b * self.importance_level()

    @classmethod
    def find(cls, _word: str, language: Language):
            return (cls.query.filter(cls.word == _word)
                    .filter(cls.language == language)
                    .one())

    @classmethod
    def find_or_create(cls, session, _word: str, language: Language):

        try:
            return cls.find(_word, language)

        except sqlalchemy.orm.exc.NoResultFound:

            try:
                new = cls(_word, language)
                session.add(new)
                session.commit()
                return new

            except:

                for _ in range(10):
                    try:
                        session.rollback()
                        w = cls.find(_word, language)
                        print ("successfully avoided race condition. nice! ")
                        return w
                    except sqlalchemy.orm.exc.NoResultFound:
                        time.sleep(0.3)
                        continue
                    break


    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_language(cls, language):
        return (cls.query.filter(cls.language == language)
                .all())

    @classmethod
    def exists(cls, word, language):
        try:
            cls.query.filter_by(
                language=language,
                word=word
            ).one()
            return True
        except NoResultFound:
            return False
