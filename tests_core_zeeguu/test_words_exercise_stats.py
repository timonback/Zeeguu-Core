import zeeguu
from unittest import TestCase

from model_test_mixin import ModelTestMixIn
from zeeguu.model.bookmark import Bookmark
from zeeguu.model.bookmark_priority_arts import BookmarkPriorityARTS
from zeeguu.model.learner_stats.word_exercise_stats import ExerciseBasedProbability


class WordsExerciseStatsTest(ModelTestMixIn, TestCase):
    db = zeeguu.db
    user = -1

    def setUp(self):
        super(WordsExerciseStatsTest, self).setUp()
        self.user = self.mir

    def test_bookmark_priority_arts_table(self):
        # GIVEN
        self._empty_table(BookmarkPriorityARTS)

        # WHEN
        count = self._count_table(BookmarkPriorityARTS)

        # THEN
        assert (count == 0)

    def test_update_bookmark_priority(self):
        # GIVEN
        self._empty_table(BookmarkPriorityARTS)
        bookmark_count_user = self._count_table(Bookmark, (lambda x: Bookmark.user == self.user))

        # WHEN
        ExerciseBasedProbability._update_bookmark_priority(self.db, self.user)
        count = self._count_table(BookmarkPriorityARTS)

        # THEN
        assert (count == bookmark_count_user)

    def _empty_table(self, cls):
        self.session.query(cls).delete()
        self.session.commit()

    def _count_table(self, cls, filter_function=(lambda x: True)):
        return self.session.query(cls).filter(filter_function).count()
