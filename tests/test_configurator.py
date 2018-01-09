import unittest
import sys
sys.path.append('../netconflib')
from netconflib.netconf import NetConf


class TestConfigurationMethods(unittest.TestCase):

    ncl = None

    def setUp(self):
        self.ncl = NetConf("tests/config.ini")

    def test_tree(self):
        try:
            self.ncl.configure_tree_topology(0, 2, False)
        except Exception:
            self.fail("configure_tree_topology() raised exception unexpectedly!")

if __name__ == '__main__':
    unittest.main()
