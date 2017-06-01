import random
from unittest import TestCase

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

import zeeguu
from tests_core_zeeguu.model_test_mixin import ModelTestMixIn
from tests_core_zeeguu.rules.url_rule import UrlRule
from tests_core_zeeguu.rules.user_rule import UserRule
from zeeguu.model.domain_name import DomainName
from zeeguu.model.url import Url
from zeeguu.the_librarian.website_recommender import recent_domains_with_times

db = zeeguu.db


class DomainTest(ModelTestMixIn, TestCase):

    def setUp(self):
        super().setUp()
        self.user_rule = UserRule()
        self.user_rule.add_bookmarks(random.randint(1, 5))
        self.user = self.user_rule.user

    def test_url_domain(self):
        """Tests the correct retrieval of a domain from a random url

        e.g. 'https://google.com' should be retrieved from
        e.g. 'https://google.com/search'
        """
        url_random = UrlRule().url.url

        url_parts = url_random.split('//', 1)
        domain_should_be = url_parts[0] + '//' + url_parts[1].split('/', 1)[0]

        domain_to_check = Url(url_random, self.faker.word()).domain_name()

        assert domain_to_check == domain_should_be, (
            domain_should_be + " should be " + domain_to_check
        )

    def test_user_recently_visited_domains(self):
        assert len(recent_domains_with_times(self.user)) != 0

    # TODO: Discuss the necessity of this test
    def test_user_recently_visited_domains_does_not_include_android(self):
        assert not(any("android" in dom[0] for dom in recent_domains_with_times(self.user)))

    def test_one_domain_multiple_urls(self):
        """
        Tests that if multiple URLs are added to the database that their
        DomainName is not added to the database more than once
        """
        # Create an 'original' URL, which is saved to the Database
        url_random_obj_origin = UrlRule().url

        # Create a random number of URLs, each with the same DomainName
        random_num = random.randint(0, 10)
        for _ in range(0, random_num):
            url_random_extended = url_random_obj_origin.url + self.faker.word()
            _ = Url(url_random_extended, self.faker.word())

        domain_for_query = url_random_obj_origin.domain_name()

        try:
            assert DomainName.find(domain_for_query)
        except NoResultFound:
            assert False, "No domains found in database"
        except MultipleResultsFound:
            assert False, "There were multiple DomainNames in the database"

