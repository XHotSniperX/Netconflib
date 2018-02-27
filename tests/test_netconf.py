import unittest
import sys
import logging
import configparser
sys.path.append('../netconflib')
from netconflib.netconf import NetConf
from netconflib.commands import Paths
from collections import Counter

class TestConfigurationMethods(unittest.TestCase):
    """Tests the configuration methods of NetConf.
    """

    CONFIG_PATH = Paths.config_file_test
    MAX_NUM = 10
    MAX_DEGREE = 1
    config = None
    ncl = None

    # logger
    logger = None

    @classmethod
    def setUpClass(cls):
        cls.logger = logging.getLogger('test.netconflib.NetConf')
        cls.logger.info("Starting linux network configuration test...")

    def test_tree_normal(self):
        """Tests the tree configurator.
        """

        for num_nodes in range(1, self.MAX_NUM + 1, 8):
            for degree in range(1, self.MAX_DEGREE + 1):
                for root in range(0, num_nodes, 8):
                    with self.subTest(num_nodes=num_nodes, degree=degree, root=root):
                        self.logger.info(
                            "Starting subtest with %d nodes, degree=%d and root=%d.",
                            num_nodes, degree, root)
                        self.init_configurator(num_nodes)
                        self.ncl.configure_tree_topology(root, degree, False)
                        self.assertEqual(
                            len(self.ncl.topology.nodes), num_nodes)
                        for node in self.ncl.topology.nodes:
                            unique_gateways = len(
                                set(node.get_all_gateways()))
                            assert unique_gateways <= degree + \
                                1, "Node has more unique gateways than the tree's degree + parent!"

    def test_hosts_updater(self):
        """Tests whether the hosts are set correctly.
        """

        self.init_configurator(self.MAX_NUM)
        self.ncl.update_hosts_file()

        nodes = self.config.items("hosts")
        hosts = {}
        for name, addr in nodes:
            hosts[name] = addr
        num = len(hosts)

        for node in self.ncl.topology.nodes:
            self.assertEqual(len(node.hosts), num)
            to_test = {}
            for host in node.hosts:
                to_test[host.name] = host.address
            self.assertDictEqual(hosts, to_test)

    def init_configurator(self, node_count, testing=True):
        """Initializes the NetConf object
        with the desired number of nodes on the cluster.

        Arguments:
            node_count {integer} -- The number of nodes.
        """

        self.config = configparser.ConfigParser()
        config_file = open(self.CONFIG_PATH, "r")
        self.config.read_file(config_file)
        config_file.close()
        if testing:
            self.config.set("settings", "testing", "yes")
        else:
            self.config.set("settings", "testing", "no")
        self.config.remove_section("hosts")
        self.config.add_section("hosts")
        for i in range(node_count):
            host = "node{}".format(i + 1)
            address = "10.0.1.{}".format(i + 1)
            self.config.set("hosts", host, address)
        config_file = open(self.CONFIG_PATH, "w")
        self.config.write(config_file)
        config_file.close()
        self.ncl = NetConf(self.CONFIG_PATH)


if __name__ == '__main__':
    LOGGER = logging.getLogger('test')
    LOGGER.setLevel(logging.INFO)
    FH = logging.FileHandler('test.log')
    FH.setLevel(logging.INFO)
    CH = logging.StreamHandler()
    CH.setLevel(logging.INFO)
    FORMATTER = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    FH.setFormatter(FORMATTER)
    CH.setFormatter(FORMATTER)
    LOGGER.addHandler(FH)
    LOGGER.addHandler(CH)
    unittest.main()
