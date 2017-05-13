import os

# Before we load the zeeguu module
# If the configuration file path is not set, try to load it from the default location
if "ZEEGUU_CORE_CONFIG" not in os.environ:
    os.environ["ZEEGUU_CORE_CONFIG"] = os.path.expanduser('~/.config/zeeguu/core_test.cfg')
import zeeguu.model

from zeeguu.populate import create_test_db, create_minimal_test_db

from unittest import TestCase


class ModelTestMixIn(TestCase):

    def setUp(self):

        # Flask can work with multiple apps. To know which of them
        # is needed we explicitly set it here
        # zeeguu.db.app = zeeguu.app

        # self.ctx = zeeguu.app.test_request_context().push()

        # if no_need_for_db is set to True, the DB is not recreated
        # this speeds up the tests a little

        if not hasattr(self, 'no_need_for_db'):
            # if maximal populate is set to True by the subclass, before
            # invoking super.setUp() we populate the DB with the extended
            # version of the test data. otherwise, only a minimal test
            # data is created.
            if hasattr(self, 'maximal_populate'):
                create_test_db(zeeguu.db)
            else:
                create_minimal_test_db(zeeguu.db)

            self.session = zeeguu.db.session

        # Some common test fixtures
        self.mir = zeeguu.model.User.find("i@mir.lu")
        self.de = zeeguu.model.Language.find("de")
        self.en = zeeguu.model.Language.find("en")

    def tearDown(self):
        super(ModelTestMixIn, self).tearDown()
        self.de = None #if we don't do this, the test holds onto this object across runs sometimes, and
        # this messes up the test db initialization. two hours well spent... aiii iaaa!
        self.mir = None
