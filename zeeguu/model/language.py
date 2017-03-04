import zeeguu

db = zeeguu.db

class Language(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    id = db.Column(db.String(2), primary_key=True)
    name = db.Column(db.String(255), unique=True)


    def __init__(self, id, name):
        self.name = name
        self.id = id

    def __repr__(self):
        return '<Language %r>' % (self.id)

    @classmethod
    def default_learned(cls):
        return cls.find("de")

    @classmethod
    def default_native_language(cls):
        return cls.find("en")

    @classmethod
    def native_languages(cls):
        return [cls.find("en")]

    @classmethod
    def available_languages(cls):
        return list(set(cls.all()) - set([Language.find("en")]))

    @classmethod
    def find(cls, id_):
        return cls.query.filter(Language.id == id_).one()

    @classmethod
    def all(cls):
        return cls.query.filter().all()