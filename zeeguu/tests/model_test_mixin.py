import os
from unittest import TestCase

import flask_sqlalchemy
import zeeguu

from flask import Flask

# We initialize here the zeeguu.app because in several places
# in the zeeguu code it is expected especially for its config

zeeguu.app = Flask("Zeeguu-Core-Test")

config_file = os.path.expanduser('~/.zeeguu/model_test.cfg')
if os.environ.has_key("CONFIG_FILE"):
    config_file = os.environ["CONFIG_FILE"]
zeeguu.app.config.from_pyfile(config_file, silent=False) #config.cfg is in the instance folder

zeeguu.db = flask_sqlalchemy.SQLAlchemy(zeeguu.app)
print ("running with DB: "+zeeguu.app.config.get("SQLALCHEMY_DATABASE_URI")) 

# CRITICAL IMPORT: Load all the model classes so they all get initialized with the zeeguu.db object
import zeeguu.model

from zeeguu.populate import create_test_db, create_minimal_test_db


class ModelTestMixIn(TestCase):

    def setUp(self):

        # Flask can work with multiple apps. To know which of them
        # is needed we explicitly set it here
        # zeeguu.db.app = zeeguu.app

        self.ctx = zeeguu.app.test_request_context().push()

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

    def tearDown(self):
        super(ModelTestMixIn, self).tearDown()
        self.de = None #if we don't do this, the test holds onto this object across runs sometimes, and
        # this messes up the test db initialization. two hours well spent... aiii iaaa!
        self.mir = None
