from unittest import TestCase
from tests_core_zeeguu.model_test_mixin import ModelTestMixIn

from zeeguu.content_retriever.parallel_retriever import get_content_for_urls
from tests_core_zeeguu.testing_data import *


class TestContentRetrieval(ModelTestMixIn, TestCase):

    def setUp(self):
        self.no_need_for_db = True
        super(TestContentRetrieval, self).setUp()

    def test_simple_parallel_retrieval(self):
        urls = [EASIEST_STORY_URL,
                VERY_EASY_STORY_URL]

        content_and_urls = get_content_for_urls(urls, 'de')

        for each in content_and_urls:
            assert each['url']
            assert each['content']

    def test_with_redirect(self):
        content_and_urls = get_content_for_urls([URL_WITH_REDIRECT], 'de')
        assert content_and_urls
