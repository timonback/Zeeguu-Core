import os

# Before we load the zeeguu module
# If the configuration file path is not set, try to load it from the default location
from faker import Faker

if "ZEEGUU_CORE_CONFIG" not in os.environ:
    os.environ["ZEEGUU_CORE_CONFIG"] = os.path.expanduser('~/.config/zeeguu/core_test.cfg')
from zeeguu.model import *

from unittest import TestCase


class ModelTestMixIn(TestCase):
    db = zeeguu.db

    def setUp(self):
        self.faker = Faker()
        self.db.create_all()

    def tearDown(self):
        super(ModelTestMixIn, self).tearDown()
        # self.db.drop_all()
