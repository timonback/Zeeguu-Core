import os

# Before we load the zeeguu module
# If the configuration file path is not set, try to load it from the default location
from faker import Faker

if "ZEEGUU_CORE_CONFIG" not in os.environ:
    os.environ["ZEEGUU_CORE_CONFIG"] = os.path.expanduser('~/.config/zeeguu/core_test.cfg')
import zeeguu.model

from unittest import TestCase
db = zeeguu.db


class ModelTestMixIn(TestCase):

    def setUp(self):
        self.faker = Faker()
        db.create_all()

    def tearDown(self):
        db.drop_all()
