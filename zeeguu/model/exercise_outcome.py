import zeeguu

db = zeeguu.db


class ExerciseOutcome(db.Model):
    __tablename__ = 'exercise_outcome'
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    id = db.Column(db.Integer, primary_key=True)
    outcome = db.Column(db.String(255), nullable=False)
    correct = db.Column(db.Boolean, nullable=False)

    CORRECT = 'Correct'
    TOO_EASY = 'Too easy'
    SHOW_SOLUTION = 'Show solution'
    RETRY = 'Retry'
    WRONG = 'Wrong'
    TYPO = 'Typo'

    def __init__(self, outcome, correct):
        self.outcome = outcome
        self.correct = correct

    @classmethod
    def find(cls, outcome):
        return cls.query.filter_by(outcome=outcome).one()
