import random

from sqlalchemy.orm.exc import NoResultFound

from tests_core_zeeguu.rules.base_rule import BaseRule
from zeeguu.model import ExerciseOutcome


class OutcomeRule(BaseRule):
    """A Testing Rule class for ExerciseOutcomes

    Has all supported outcomes as properties. Outcomes are created and
    saved to the database if they don't yet exist in the database.
    """

    outcomes = {
        "Show Solution": False,
        "Retry": False,
        "Correct": True,
        "Wrong": False,
        "Typo": False,
        "Too easy": True
    }

    @classmethod
    def __get_or_create_outcome(cls, outcome):
        try:
            return ExerciseOutcome.find(outcome)
        except NoResultFound:
            return cls.__create_new_outcome(outcome)

    @classmethod
    def __create_new_outcome(cls, outcome):
        correct = cls.outcomes.get(outcome)

        if correct is None:
            raise KeyError

        new_outcome = ExerciseOutcome(outcome, correct)

        cls.save(new_outcome)

        return new_outcome

    @property
    def show_solution(self):
        return self.__get_or_create_outcome("Show Solution")

    @property
    def retry(self):
        return self.__get_or_create_outcome("Retry")

    @property
    def correct(self):
        return self.__get_or_create_outcome("Correct")

    @property
    def wrong(self):
        return self.__get_or_create_outcome("Wrong")

    @property
    def typo(self):
        return self.__get_or_create_outcome("Typo")

    @property
    def too_easy(self):
        return self.__get_or_create_outcome("Too Easy")

    @property
    def random(self):
        random_outcome, __ = random.choice(list(self.outcomes.items()))
        return self.__get_or_create_outcome(random_outcome)
