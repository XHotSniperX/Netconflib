import unittest
import sys
import configparser
sys.path.append('../netconflib')
from netconflib.netconf import NetConf


class TestConfigurationMethods(unittest.TestCase):
    """Tests the configuration methods of NetConf.
    """

    CONFIG_PATH = "tests/config.ini"
    NUM = 64
    config = None
    ncl = None

    def setUp(self):
        self.config = configparser.ConfigParser()
        config_file = open(self.CONFIG_PATH, "r")
        self.config.read_file(config_file)
        config_file.close()
        self.config.remove_section("hosts")
        self.config.add_section("hosts")
        for i in range(self.NUM):
            host = "node{}".format(i + 1)
            address = "10.0.1.{}".format(i + 1)
            self.config.set("hosts", host, address)
        config_file = open(self.CONFIG_PATH, "w")
        self.config.write(config_file)
        config_file.close()
        self.ncl = NetConf(self.CONFIG_PATH)

    def test_tree(self):
        """Tests the tree configurator.
        """

        try:
            self.ncl.configure_tree_topology(0, 2, False)
        except Exception:
            self.fail("configure_tree_topology() raised exception unexpectedly!")

if __name__ == '__main__':
    unittest.main()
