from unittest import TestCase

import zeeguu
from tests_core_zeeguu.model_test_mixin import ModelTestMixIn

db = zeeguu.db
from zeeguu.model.domain_name import DomainName
from zeeguu.model.url import Url

from zeeguu.the_librarian.website_recommender import recent_domains_with_times


class DomainTest(ModelTestMixIn, TestCase):

    def setUp(self):
        self.maximal_populate = True
        super(DomainTest, self).setUp()

    def test_url_domain(self):

        url = Url.find_or_create("http://news.mir.com/page1", "Mir News")
        assert url.domain_name() == "http://news.mir.com"

        url = Url.find_or_create("news.mir.com/page1", "Mir News")
        assert url.domain_name() == "news.mir.com"

        url = Url.find_or_create("", "Mir News")
        assert url.domain_name() == ""

    def test_user_recently_visited_domains(self):
        assert len(recent_domains_with_times(self.mir)) == 3

    def test_user_recently_visited_domains_does_not_include_android(self):
        assert not(any("android" in dom[0] for dom in recent_domains_with_times(self.mir)))

    def test_one_domain_multiple_urls(self):
        # Funny thing: you have to make sure to commit ASAP
        # otherwise, you end up having two domain name objects
        # because each Url creates one...
        u1 = Url("https://mir.lu/tralala/trilili", "")
        db.session.add(u1)
        db.session.commit()

        u2 = Url("https://mir.lu/tralala/trilili2", "")
        db.session.add(u2)
        db.session.commit()

        d = DomainName.find("https://mir.lu")
        assert str(d)
