import zeeguu

db = zeeguu.db


class ExerciseSource(db.Model):
    __tablename__ = 'exercise_source'
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(255), nullable=False)

    def __init__(self, source):
        self.source = source

    @classmethod
    def find(cls, source):
        return cls.query.filter_by(source=source).one()
