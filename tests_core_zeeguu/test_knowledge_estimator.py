from datetime import datetime
from unittest import TestCase

from zeeguu.algos.algo_service import AlgoService

from tests_core_zeeguu.model_test_mixin import ModelTestMixIn

import zeeguu
db = zeeguu.db
from zeeguu.model.exercise import Exercise
from zeeguu.model.exercise_outcome import ExerciseOutcome
from zeeguu.model.exercise_source import ExerciseSource
from zeeguu.model.knowledge_estimator import SimpleKnowledgeEstimator


class FeedTest(ModelTestMixIn, TestCase):

    def test_words_being_learned(self):
        est = SimpleKnowledgeEstimator(self.mir)
        #TODO fix test
        #assert len(est.words_being_learned()) == 2

    def test_get_known_bookmarks(self):
        est = SimpleKnowledgeEstimator(self.mir)
        before = est.get_known_bookmarks()

        b0 = self.mir.all_bookmarks()[0]
        ex = Exercise(ExerciseOutcome.find(ExerciseOutcome.TOO_EASY), ExerciseSource.find_by_source("Recognize"), 100, datetime.now())
        b0.add_new_exercise(ex)

        db.session.add(b0)
        db.session.commit()

        AlgoService.update_bookmark_priority(db, self.mir)

        after = est.get_known_bookmarks()

        assert len(after) >= len(before)

