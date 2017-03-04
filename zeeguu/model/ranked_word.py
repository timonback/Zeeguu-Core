import sqlalchemy.orm
import zeeguu
from zeeguu import util
from zeeguu.model.language import Language


class RankedWord(zeeguu.db.Model, util.JSONSerializable):
    __tablename__ = 'ranked_word'
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    id = zeeguu.db.Column(zeeguu.db.Integer, primary_key=True)
    word = zeeguu.db.Column(zeeguu.db.String(255), nullable =False, index = True)

    language_id = zeeguu.db.Column(zeeguu.db.String(2), zeeguu.db.ForeignKey("language.id"))
    language = zeeguu.db.relationship("Language")
    rank = zeeguu.db.Column(zeeguu.db.Integer)
    zeeguu.db.UniqueConstraint(word, language_id)

    ranked_words_cache = {}

    def __init__(self, word, language, rank):
        self.word = word
        self.language = language
        self.rank = rank

    def set_rank(self, new_rank):
        self.rank = new_rank

    @classmethod
    def find(cls, word, language):
        word = word.lower()
        try:
            return (cls.query.filter(cls.word == word)
                             .filter(cls.language == language)
                             .one())
        except sqlalchemy.orm.exc.NoResultFound:
            return None

    @classmethod
    def find_all(cls,language):
        return cls.query.filter(cls.language == language
        ).all()

    @classmethod
    def exists(cls, word, language):
        word = word.lower()
        try:
            (cls.query.filter(cls.word == word)
                             .filter(cls.language == language)
                             .one())
            return True
        except sqlalchemy.orm.exc.NoResultFound:
            return False

    @classmethod
    def words_list(cls):
        words_list = []
        for word in cls.find_all():
             words_list.append(word.word)
        return words_list

    @classmethod
    def cache_ranked_words(cls):
        cls.ranked_words_cache = {}
        for language in Language.all():
            ranked_words = cls.find_all(language)
            for ranked_word in ranked_words:
                ranked_word_key = language.id + '_' + ranked_word.word
                cls.ranked_words_cache[ranked_word_key] = ranked_word

    @classmethod
    def find_cache(cls, word, language):
        try:
            ranked_word_key = language.id + '_' + word.lower()
            return cls.ranked_words_cache[ranked_word_key]
        except KeyError:
            return None