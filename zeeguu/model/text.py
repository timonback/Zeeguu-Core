import re

import sqlalchemy.orm
import time
import zeeguu

from zeeguu.util import text_hash
from zeeguu.model.language import Language
from zeeguu.model.url import Url
from zeeguu.model.user_word import UserWord

db = zeeguu.db


class Text(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(10000))

    content_hash = db.Column(db.String(255))

    language_id = db.Column(db.String(2), db.ForeignKey(Language.id))
    language = db.relationship(Language)

    url_id = db.Column(db.Integer, db.ForeignKey(Url.id))
    url = db.relationship(Url)

    def __init__(self, content, language, url):
        self.content = content
        self.language = language
        self.url = url
        self.content_hash = text_hash(content)

    def __repr__(self):
        return '<Text %r>' % (self.content)

    def words(self):
        for word in re.split(re.compile("[^\\w]+", re.U), self.content):
            yield UserWord.find(word, self.language)

    def shorten_word_context(self, given_word, max_word_count):
        # shorter_text = ""
        limited_words=[]

        words = self.content.split() # ==> gives me a list of the words ["these", "types", ",", "the"]
        word_count = len(words)

        if word_count <= max_word_count:
            return self.content

        for i in range(0, max_word_count):
            limited_words.append(words[i]) # lista cu primele max_length cuvinte
        shorter_text = ' '.join(limited_words) # string cu primele 'max_word_count' cuv

        # sometimes the given_word does not exist in the text.
        # in that case return a text containing max_length words
        if given_word not in words:
            return shorter_text

        if words.index(given_word) <= max_word_count:
            return shorter_text

        for i in range(max_word_count + 1,  words.index(given_word) + 1):
            limited_words.append(words[i])
        shorter_text = ' '.join(limited_words)

        return shorter_text

    def all_bookmarks(self, user):
        from zeeguu.model import Bookmark
        return Bookmark.find_all_for_user_and_text(self, user)

    @classmethod
    def find_or_create(cls, session, text, language, url):
        """
        :param text: string
        :param language: Language (object)
        :param url: Url (object)
        :return:
        """

        try:
            return cls.query.filter(cls.content_hash == text_hash(text)).one()
        except sqlalchemy.orm.exc.NoResultFound or sqlalchemy.exc.InterfaceError:
            try:
                new = cls(text, language, url)
                session.add(new)
                session.commit()
                return new
            except sqlalchemy.exc.IntegrityError or sqlalchemy.exc.DatabaseError:
                for i in range(10):
                    try:
                        session.rollback()
                        t = cls.query.filter(cls.content_hash == text_hash(text)).one()
                        print("found text after recovering from race")
                        return t
                    except:
                        print("exception of second degree in find text..." + str(i))
                        time.sleep(0.3)
                        continue
                    break

