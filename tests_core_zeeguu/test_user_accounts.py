from unittest import TestCase

import zeeguu
from zeeguu import util
from tests_core_zeeguu.model_test_mixin import ModelTestMixIn
from zeeguu.model import Session, User

WANNABE_UUID = '2b4a7c0d1e8f'
TEST_PASS = 'cherrypie'

class UserPreferenceTest(ModelTestMixIn, TestCase):


    def setUp(self):
        self.maximal_populate = True
        super(UserPreferenceTest, self).setUp()

    #
    def test_password_hash(self):
        user = User.find("i@mir.lu")
        hash1 = util.password_hash("test" ,user.password_salt)
        hash2 = util.password_hash("wrong", user.password_salt)

        assert hash1 != hash2
        assert user.authorize("i@mir.lu", "test") != None

    # TODO: must commit the first session first.
    def test_user_session(self):
        user = User.find("i@mir.lu")
        s = Session.find_for_user(user)
        # print s.id
        zeeguu.db.session.add(s)
        zeeguu.db.session.commit()

        # print s.id
        # #
        # s2 = Session.find_for_id(s.id)
        # print s2
        # assert (s2.user == user)
        #
        # s3 = Session.find_for_id(3)
        # assert not s3

    def test_create_anonymous_user_and_get_sessions(self):
        u1 = User.create_anonymous(WANNABE_UUID, TEST_PASS, 'de')
        zeeguu.db.session.add_all([u1])
        zeeguu.db.session.commit()
        assert u1.name == WANNABE_UUID
        return u1

    def test_get_session_for_anonymous_user(self):
        self.test_create_anonymous_user_and_get_sessions()
        user = User.authorize(WANNABE_UUID+'@mir.lu',TEST_PASS)
        assert Session.find_for_user(user).id > 0

    def test_even_anonumous_users_have_to_study(self):
        u1 = self.test_create_anonymous_user_and_get_sessions()
        assert len(u1.bookmarks_to_study(4)) == 4