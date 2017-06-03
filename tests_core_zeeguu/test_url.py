from unittest import TestCase


from tests_core_zeeguu.model_test_mixin import ModelTestMixIn
from tests_core_zeeguu.rules.url_rule import UrlRule

import zeeguu
from zeeguu.model import Url

db = zeeguu.db


class UrlTest(ModelTestMixIn, TestCase):

    def setUp(self):
        super().setUp()
        self.url_rule = UrlRule()
        print ("done with setup")

    def test_domain_plus_path_must_be_unique(self):

        _url = self.url_rule.url.as_string()
        _title = self.url_rule.url.title

        session = zeeguu.db.session

        with self.assertRaises(Exception) as context:

            url = Url(_url, _title)
            session.add(url)
            session.commit()

        print (str(context.exception))
        self.assertTrue('Duplicate entry' in str(context.exception))






