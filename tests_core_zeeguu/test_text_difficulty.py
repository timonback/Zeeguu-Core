# -*- coding: utf8 -*-

from unittest import TestCase

import zeeguu

from tests_core_zeeguu.model_test_mixin import ModelTestMixIn
from zeeguu.model.feed import RSSFeed
from zeeguu.model.url import Url

SIMPLE_TEXT = "Das ist "
COMPLEX_TEXT = "Alle hatten in sein Lachen eingestimmt, hauptsächlich aus Ehrerbietung " \
               "gegen das Familienoberhaupt"


class TextDifficultyTest(ModelTestMixIn, TestCase):

    def setUp(self):
        self.maximal_populate = True
        super(TextDifficultyTest, self).setUp()

    def very_simple_test(self):

        d1 = self.mir.text_difficulty(SIMPLE_TEXT, self.de)
        d2 = self.mir.text_difficulty(COMPLEX_TEXT, self.de)

        assert d1['estimated_difficulty'] == 'EASY'
        assert d1['score_average'] < 0.1
        assert d1['score_median'] < 0.1

        assert d2 > d1

    def test_difficulty_of_text_at_url(self):
        url = Url("http://www.bild.de/rss-feeds/rss-16725492,feed=home.bild.html", "Build")
        zeeguu.db.session.add(url)
        zeeguu.db.session.commit()

        print(url.as_string())
        print(url.id)

        feed = RSSFeed(url, "Bild.de Home", "build", image_url=None, language=None)
        first_item = feed.feed_items()[0]
        print(first_item['url'])

