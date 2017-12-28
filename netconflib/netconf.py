# -*- coding: utf-8 -*-
"""A linux cluster configuration library.

Use this library to simply configure the network topology of a linux cluster.
"""

import configparser
import logging
from .ssh import SSH
from .commands import Commands


class NetConf:
    """Configuration library

    This class provides methods to configure the network
    of a Linux cluster.
    """

    # logger
    logger = None
    # number of nodes
    num_nodes = 0
    # host addresses
    nodes = []
    # connections to nodes
    connections = []
    # authentication
    username = ""
    password = ""

    cmds = None
    config = None

    def __init__(self, configfile):
        self.logger = logging.getLogger('app.netconflib.NetConf')
        self.logger.info("Starting linux network configuration...")
        # Load the configuration file
        self.config = configparser.ConfigParser()
        self.config.read(configfile)
        self.cmds = Commands()
        self.nodes = self.config.items("hosts")
        self.num_nodes = len(self.nodes)
        self.username = self.config.get("authentication", "username")
        self.password = self.config.get("authentication", "password")

        self.logger.info("Testing connection to all specified nodes...")
        try:
            for node, addr in self.nodes:
                self.logger.debug(
                    "Creating new connection to {}, {} and adding it to list of connections...".format(node, addr))
                self.connections.append(
                    SSH(addr, self.username, self.password))
        except Exception as ex:
            self.logger.error(ex)
            self.logger.error("connection test failed. Exiting...")
            exit(1)
        self.logger.info("Successfully connected to all nodes.")

    def enable_ip_forwarding(self):
        """Enables ip packet forwarding on every node on the cluster."""
        self.logger.info("Enabling IP packet forwarding...")
        for c in self.connections:
            c.send_command(self.cmds.cmd_ipforward)

    def update_hosts_file(self):
        """Appends all the ip addresses and host names to etc/hosts file."""
        for i, c in enumerate(self.connections):
            self.logger.debug(
                "Node{}: Adding host entries to /etc/hosts file...".format(i + 1))
            for j in range(0, self.num_nodes):
                if j == i:
                    self.logger.debug(
                        "127.0.1.1    {}".format(self.nodes[j][0]))
                    c.send_command(
                        "echo '127.0.1.1    {}' | sudo tee -a /etc/hosts".format(self.nodes[j][0]))
                else:
                    self.logger.debug("{}   {}".format(
                        self.nodes[j][1], self.nodes[j][0]))
                    c.send_command(
                        "echo '{}   {}' | sudo tee -a /etc/hosts".format(self.nodes[j][1], self.nodes[j][0]))

    def configure_ring_topology(self):
        """Configures the cluster's network topology as a ring."""
        for i, c in enumerate(self.connections):
            self.logger.debug("Node{}:".format(i + 1))
            for j in range(0, self.num_nodes):
                if j == i:
                    continue
                self.logger.debug("route add -host {} gw {}".format(
                    self.nodes[j][0], self.nodes[(i + 1) % (self.num_nodes)][0]))
                c.send_command("sudo route add -host {} gw {}".format(
                    self.nodes[j][0], self.nodes[(i + 1) % (self.num_nodes)][0]))

    def remove_ring_topology(self):
        """Removes the ring netork topology from the cluster."""
        for i, c in enumerate(self.connections):
            self.logger.debug("Node{}:".format(i + 1))
            for j in range(0, self.num_nodes):
                if j == i:
                    continue
                self.logger.debug("route del -host {} gw {}".format(
                    self.nodes[j][0], self.nodes[(i + 1) % (self.num_nodes)][0]))
                c.send_command("sudo route del -host {} gw {}".format(
                    self.nodes[j][0], self.nodes[(i + 1) % (self.num_nodes)][0]))
