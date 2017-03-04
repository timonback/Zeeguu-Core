from unittest import TestCase
from zeeguu import util
from zeeguu.tests.model_tests.model_test_mixin import ModelTestMixIn
from zeeguu.model import Session, User


class UserPreferenceTest(ModelTestMixIn, TestCase):

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
        # #
        # s2 = Session.find_for_id(s.id)
        # print s2
        # assert (s2.user == user)
        #
        # s3 = Session.find_for_id(3)
        # assert not s3
