import os

# Before we load the zeeguu module
# If the configuration file path is not set, try to load it from the default location

if "ZEEGUU_CORE_CONFIG" not in os.environ:
    os.environ["ZEEGUU_CORE_CONFIG"] = os.path.expanduser('~/.config/zeeguu/core_test.cfg')

from unittest import TestCase


class ModelTestMixIn(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
