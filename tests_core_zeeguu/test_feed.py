from unittest import TestCase

from tests_core_zeeguu.model_test_mixin import ModelTestMixIn
from zeeguu.model.feed import RSSFeed
from zeeguu.model.url import Url


class FeedTest(ModelTestMixIn, TestCase):
    def test_feed_items(self):
        url = Url(
            "http://www.bild.de/rss-feeds/rss-16725492,feed=home.bild.html",
            "Build")
        feed = RSSFeed(url, "Bild.de Home", "build", image_url=None,
                       language=None)
        items = feed.feed_items()

        first_item_date = items[0]["published"]
        assert first_item_date
