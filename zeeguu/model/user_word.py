import sqlalchemy.orm
from wordstats import Word

from zeeguu import util
import zeeguu
db = zeeguu.db

from zeeguu.model.language import Language


class UserWord(db.Model, util.JSONSerializable):
    __tablename__ = 'user_word'
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(255), nullable =False, unique = True)
    language_id = db.Column(db.String(2), db.ForeignKey("language.id"))
    language = db.relationship("Language")
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
    def find(cls, word, language):
        try:
            return (cls.query.filter(cls.word == word)
                             .filter(cls.language == language)
                             .one())
        except sqlalchemy.orm.exc.NoResultFound as e:
            return cls(word, language)


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