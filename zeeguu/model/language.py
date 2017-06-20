from sqlalchemy.orm.exc import NoResultFound

import zeeguu

db = zeeguu.db


class Language(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_bin'}
    __tablename__ = 'language'

    id = db.Column(db.String(2), primary_key=True)
    name = db.Column(db.String(255), unique=True)

    languages = {
        "de": "German",
        "en": "English",
        "es": "Spanish",
        "fr": "French",
        "nl": "Dutch"
    }

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Language %r>' % self.id

    def __eq__(self, other):
        return self.id == other.id or self.name == other.name

    @classmethod
    def default_learned(cls):
        return cls.find_or_create("de")

    @classmethod
    def default_native_language(cls):
        return cls.find_or_create("en")

    @classmethod
    def native_languages(cls):
        return [cls.find_or_create("en")]

    @classmethod
    def available_languages(cls):
        return [Language.find_or_create('de'), Language.find_or_create('es'), Language.find_or_create('fr'), Language.find_or_create('nl')]

    @classmethod
    def find(cls, id_):
        return cls.query.filter(Language.id == id_).one()

    @classmethod
    def find_or_create(cls, language_id):
        try:
            language = cls.find(language_id)

        except NoResultFound:
            language = cls(language_id, cls.languages[language_id])
            db.session.add(language)
            db.session.commit()

        return language

    @classmethod
    def all(cls):
        return cls.query.filter().all()
