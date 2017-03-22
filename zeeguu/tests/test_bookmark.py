from zeeguu.tests.model_test_mixin import ModelTestMixIn
from zeeguu.model.learner_stats.word_encounter_stats import EncounterStats

import random
import unittest
from datetime import datetime
from unittest import TestCase

from zeeguu.model import Bookmark, UserWord


class BookmarkTest(ModelTestMixIn, TestCase):

    def setUp(self):
        super(BookmarkTest, self).setUp()
        self.first_bookmark = self.mir.all_bookmarks()[0]

    def test_user_bookmark_count(self):
        assert len(self.mir.all_bookmarks()) > 0
        print self.mir.all_bookmarks()

    def test_bookmark_is_serializable(self):
        print self.first_bookmark.json_serializable_dict()

    def test_user_daily_bookmarks(self):

        date = datetime(2011,01,01,01,01,01)

        assert len(self.mir.all_bookmarks()) > 0

        count_bookmarks = 0
        for bookmark in self.mir.all_bookmarks():
            if bookmark.time == date:
                count_bookmarks += 1

        assert (count_bookmarks > 0)

    def test_importance_level(self):

        mutter = UserWord.find("mutter", self.de)
        reg = UserWord.find("regierung", self.de)
        assert mutter.importance_level() == 10
        assert reg.importance_level() == 8

    def test_update_encounter_stats(self):

        assert len(EncounterStats.find_all(self.mir, self.de.id)) == 0

        self.first_bookmark. \
            update_encounter_stats_after_adding_a_bookmark(
            self.mir,
            self.de)

        assert len(EncounterStats.find_all(self.mir, self.de.id)) > 0

