import zeeguu
from sqlalchemy.sql import func

from zeeguu.model.exercise_source import ExerciseSource

db = zeeguu.db


class ExerciseStats(db.Model):

    __tablename__ = 'algo_stats'
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    exercise_source_id = db.Column(db.Integer, db.ForeignKey("exercise_source.id"), primary_key=True)
    exercise_source = db.relationship(ExerciseSource)

    mean = db.Column(db.DECIMAL(10, 3), nullable=False)
    sd = db.Column(db.DECIMAL(10, 3), nullable=False)

    updated = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    db.CheckConstraint('mean>=0', 'sd>=0')

    def __init__(self, exercise_source, mean, sd):
        self.exercise_source = exercise_source
        self.mean = mean
        self.sd = sd
