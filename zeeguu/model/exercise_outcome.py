import sqlalchemy
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

    correct_outcomes = [
        CORRECT,
        TOO_EASY
    ]

    def __init__(self, outcome):
        self.outcome = outcome

    def __eq__(self, other):
        return self.outcome == other.outcome and self.correct == other.correct

    @property
    def correct(self):
        return self.outcome in self.correct_outcomes

    @classmethod
    def find(cls, outcome: str):
        return cls.query.filter_by(outcome=outcome).one()

    @classmethod
    def find_or_create(cls, session, _outcome: str):
        try:
            outcome = cls.find(_outcome)

        except sqlalchemy.orm.exc.NoResultFound as e:
            outcome = cls(_outcome)
        except Exception as e:
            raise e

        session.add(outcome)
        session.commit()

        return outcome
