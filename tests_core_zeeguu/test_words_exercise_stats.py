from unittest import TestCase

import zeeguu
from tests_core_zeeguu.model_test_mixin import ModelTestMixIn
from zeeguu.model.bookmark import Bookmark
from zeeguu.model.bookmark_priority_arts import BookmarkPriorityARTS
from zeeguu.model.learner_stats.word_exercise_stats import AlgoService


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
        bookmark_count_user = self._count_table(Bookmark,
                                                Bookmark.user == self.user)

        # WHEN
        AlgoService.update_bookmark_priority(self.db, self.user)
        count = self._count_table(BookmarkPriorityARTS)

        # THEN
        assert (bookmark_count_user == count), (
        str(bookmark_count_user) + ' should be == to ' + str(count))

    def _empty_table(self, cls):
        self.db.session.query(cls).delete()
        self.db.session.commit()

    def _count_table(self, cls, filter=True):
        return self.db.session.query(cls).filter(filter).count()
