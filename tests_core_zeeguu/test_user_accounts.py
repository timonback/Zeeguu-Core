from tests_core_zeeguu.model_test_mixin import ModelTestMixIn
from tests_core_zeeguu.rules.user_rule import UserRule

WANNABE_UUID = '2b4a7c0d1e8f'
TEST_PASS = 'cherrypie'


class UserPreferenceTest(ModelTestMixIn):
    def setUp(self):
        super().setUp()
        self.user = UserRule().user

    # TODO: Discuss why they implement their own hashing algorithm
        # def test_password_hash(self):
        #    assert False
        # hash1 = util.password_hash("test", user.password_salt)
        # hash2 = util.password_hash("wrong", user.password_salt)
        #
        # assert hash1 != hash2
        # assert user.authorize("i@mir.lu", "test") != None

    # TODO: What is the meaning of the following tests?
        # def test_user_session(self):
        #    assert False
        # s = Session.find_for_user(self.user)


        # @staticmethod
        # def test_create_anonymous_user_and_get_sessions():
        #    assert False
        # u1 = User.create_anonymous(WANNABE_UUID, TEST_PASS, 'de')
        # zeeguu.db.session.add_all([u1])
        # zeeguu.db.session.commit()
        # assert u1.name == WANNABE_UUID

        # @classmethod
        # def test_get_session_for_anonymous_user(cls):
        #    assert False
        # cls.test_create_anonymous_user_and_get_sessions()
        # user = User.authorize(WANNABE_UUID + '@mir.lu', TEST_PASS)
        # assert Session.find_for_user(user).id > 0
        # s3 = Session.find_for_id(3)
    #   # assert not s3
    #
    # @staticmethod
    # def test_create_anonymous_user_and_get_sessions():
    #     u1 = User.create_anonymous(WANNABE_UUID, TEST_PASS, 'de')
    #     zeeguu.db.session.add_all([u1])
    #     zeeguu.db.session.commit()
    #     assert u1.name == WANNABE_UUID
    #
    # @classmethod
    # def test_get_session_for_anonymous_user(cls):
    #     cls.test_create_anonymous_user_and_get_sessions()
    #     user = User.authorize(WANNABE_UUID+'@mir.lu',TEST_PASS)
    #     assert Session.find_for_user(user).id > 0
    #
    # def test_even_anonumous_users_have_to_study(self):
    #     u1 = User.create_anonymous(WANNABE_UUID, TEST_PASS, 'de')
    #     zeeguu.db.session.add_all([u1])
    #     zeeguu.db.session.commit()
    #     self.assertIsNotNone(u1.bookmarks_to_study(4))
