# -*- coding: utf8 -*-

from unittest import TestCase

import zeeguu

from tests_core_zeeguu.model_test_mixin import ModelTestMixIn
from tests_core_zeeguu.rules.language_rule import LanguageRule
from tests_core_zeeguu.rules.user_rule import UserRule
from zeeguu.model.feed import RSSFeed
from zeeguu.model.url import Url

SIMPLE_TEXT = "Das ist "
COMPLEX_TEXT = "Alle hatten in sein Lachen eingestimmt, hauptsächlich aus Ehrerbietung " \
               "gegen das Familienoberhaupt"


class TextDifficultyTest(ModelTestMixIn, TestCase):

    def setUp(self):
        super().setUp()
        self.user = UserRule().user
        self.lan = LanguageRule().de

    def test_compute_very_simple_text_difficulty(self):

        d1 = self.user.text_difficulty(SIMPLE_TEXT, self.lan)
        d2 = self.user.text_difficulty(COMPLEX_TEXT, self.lan)

        assert d1['estimated_difficulty'] == 'EASY'
        assert d1['score_average'] < 0.1
        assert d1['score_median'] < 0.1

    # TODO: What does the following test do?
    # def test_difficulty_of_text_at_url(self):
    #     url = Url("http://www.bild.de/rss-feeds/rss-16725492,feed=home.bild.html", "Build")
    #     zeeguu.db.session.add(url)
    #     zeeguu.db.session.commit()
    #
    #     feed = RSSFeed(url, "Bild.de Home", "build", image_url=None, language=None)
    #     first_item = feed.feed_items()[0]

