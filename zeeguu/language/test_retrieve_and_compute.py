from unittest import TestCase


from zeeguu.tests.model_test_mixin import ModelTestMixIn

from zeeguu.model import Url, RSSFeed

from zeeguu.language.retrieve_and_compute import retrieve_urls_and_compute_metrics
from zeeguu.model import RankedWord
from zeeguu.tests.testing_data import *


class TestRetrieveAndCompute(ModelTestMixIn, TestCase):

    def setUp(self):
        self.maximal_populate = True
        super(TestRetrieveAndCompute, self).setUp()
        RankedWord.cache_ranked_words()

    def testSimple(self):

        urls = [EASIEST_STORY_URL,
                VERY_EASY_STORY_URL,
                EASY_STORY_URL]

        difficulties = retrieve_urls_and_compute_metrics(urls,
                                                         self.de,
                                                         self.mir)

        difficulty_for_easiest = difficulties[EASIEST_STORY_URL]['difficulty']
        difficulty_for_very_easy = difficulties[VERY_EASY_STORY_URL]['difficulty']
        difficulty_for_easy = difficulties[EASY_STORY_URL]['difficulty']

        assert \
            difficulty_for_easiest['normalized'] < \
            difficulty_for_easy['normalized']

        # on the other hand, they're all EASY
        assert difficulty_for_easiest['discrete'] == difficulty_for_very_easy['discrete']

    def testDifficultyOfFeedItems(self):
        url = Url(DE_SAMPLE_FEED_1_URL, DE_SAMPLE_FEED_1_URL)
        feed = RSSFeed(url, DE_SAMPLE_FEED_1_TITLE, "blabla", image_url = None, language = self.de)

        items_with_metrics = feed.feed_items_with_metrics(self.mir, 5)

        assert len(items_with_metrics) > 0
        assert items_with_metrics[0]["title"]
        assert items_with_metrics[0]["summary"]
        assert items_with_metrics[0]["published"]

        print items_with_metrics[0]["title"]
        print items_with_metrics[0]["metrics"]



