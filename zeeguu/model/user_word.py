import sqlalchemy.orm

from zeeguu import util
from zeeguu.model.ranked_word import RankedWord
import zeeguu
db = zeeguu.db

class UserWord(db.Model, util.JSONSerializable):
    __tablename__ = 'user_word'
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(255), nullable =False, unique = True)
    language_id = db.Column(db.String(2), db.ForeignKey("language.id"))
    language = db.relationship("Language")
    rank_id = db.Column(db.Integer, db.ForeignKey("ranked_word.id"), nullable=True)
    rank = db.relationship("RankedWord")
    db.UniqueConstraint(word, language_id)

    IMPORTANCE_LEVEL_STEP = 1000
    IMPOSSIBLE_RANK = 1000000
    IMPOSSIBLE_IMPORTANCE_LEVEL = IMPOSSIBLE_RANK / IMPORTANCE_LEVEL_STEP

    def __init__(self, word, language, rank = None):
        self.word = word
        self.language = language
        self.rank = rank

    def set_rank(self, new_rank):
        self.rank = new_rank

    def __repr__(self):
        return '<UserWord %r>' % (self.word)

    def serialize(self):
        return self.word

    # returns a number between
    def importance_level(self):
        if self.rank is not None:
            return max((10 - self.rank.rank / UserWord.IMPORTANCE_LEVEL_STEP), 0)
        else:
            return  0

    # returns the rank if in the DB, or the impossible rank
    def get_rank(self):
        if self.rank is not None:
            return self.rank.rank
        else:
            return UserWord.IMPOSSIBLE_RANK


    # we use this in the bookmarks.html to show the rank.
    # for words in which there is no rank info, we don't display anything
    def importance_level_string(self):
        if self.rank == None:
            return ""
        b = "|"
        return b * self.importance_level()

    @classmethod
    def find(cls, word, language):
        try:
            return (cls.query.filter(cls.word == word)
                             .filter(cls.language == language)
                             .one())
        except sqlalchemy.orm.exc.NoResultFound as e:
            rank = UserWord.find_rank(word.lower(),language)
            return cls(word, language,rank)


    @classmethod
    def find_rank(cls, word, language):
        return RankedWord.find(word, language)

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
                language = language,
                word = word
            ).one()
            return True
         except  sqlalchemy.orm.exc.NoResultFound:
            return False