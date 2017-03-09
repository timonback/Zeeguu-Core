# -*- coding: utf8 -*-

from unittest import TestCase

import zeeguu
from zeeguu.tests.model_test_mixin import ModelTestMixIn

from zeeguu.model import RSSFeed
from zeeguu.model import Url
from zeeguu.model import RankedWord

SIMPLE_TEXT = "Das ist "
COMPLEX_TEXT = u"Alle hatten in sein Lachen eingestimmt, hauptsächlich aus Ehrerbietung " \
               u"gegen das Familienoberhaupt"


class TextDifficultyTest(ModelTestMixIn, TestCase):

    def setUp(self):
        self.maximal_populate = True
        super(TextDifficultyTest, self).setUp()
        RankedWord.cache_ranked_words()

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

        print url.as_string()
        print url.id

        feed = RSSFeed(url, "Bild.de Home", "build", image_url=None, language=None)
        first_item = feed.feed_items()[0]
        print first_item['url']

