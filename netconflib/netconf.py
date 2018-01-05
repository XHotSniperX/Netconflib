# -*- coding: utf-8 -*-
"""A linux cluster configuration library.

Use this library to simply configure the network topology of a linux cluster.
"""

import configparser
import logging
from treelib import Tree
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
    testing = False

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
        self.testing = self.config.get("settings", "testing")

        if not self.testing:
            self.logger.info("Establishing connection to all specified nodes...")
            try:
                for node, addr in self.nodes:
                    self.logger.debug(
                        "Creating new connection to {}, {} and adding it to list of connections...".format(node, addr))
                    self.connections.append(
                        SSH(addr, self.username, self.password))
            except Exception as ex:
                self.logger.error(ex)
                self.logger.error("connection failed with {}.".format(node))
            self.logger.info("Connections established.")

    def enable_ip_forwarding(self):
        """Enables ip packet forwarding on every node on the cluster."""
        self.logger.info("Enabling IP packet forwarding...")
        for c in self.connections:
            if not self.testing:
                c.send_command(self.cmds.cmd_ipforward)

    def update_hosts_file(self):
        """Appends all the ip addresses and host names to etc/hosts file."""
        for i in range(self.num_nodes):
            self.logger.debug(
                "Node{}: Adding host entries to /etc/hosts file...".format(i + 1))
            for j in range(0, self.num_nodes):
                if j == i:
                    self.logger.debug(
                        "127.0.1.1    {}".format(self.nodes[j][0]))
                    if not self.testing:
                        self.connections[i].send_command(
                            "echo '127.0.1.1    {}' | sudo tee -a /etc/hosts".format(self.nodes[j][0]))
                else:
                    self.logger.debug("{}   {}".format(
                        self.nodes[j][1], self.nodes[j][0]))
                    if not self.testing:
                        self.connections[i].send_command(
                            "echo '{}   {}' | sudo tee -a /etc/hosts".format(self.nodes[j][1], self.nodes[j][0]))

    def configure_ring_topology(self):
        """Configures the cluster's network topology as a ring."""
        for i in range(self.num_nodes):
            self.logger.debug("Node{}:".format(i + 1))
            for j in range(0, self.num_nodes):
                if j == i:
                    continue
                self.logger.debug("sudo route add -host {} gw {}".format(
                    self.nodes[j][0], self.nodes[(i + 1) % (self.num_nodes)][0]))
                if not self.testing:
                    self.connections[i].send_command("sudo route add -host {} gw {}".format(
                        self.nodes[j][0], self.nodes[(i + 1) % (self.num_nodes)][0]))

    def remove_ring_topology(self):
        """Removes the ring netork topology from the cluster."""
        for i in range(self.num_nodes):
            self.logger.debug("Node{}:".format(i + 1))
            for j in range(0, self.num_nodes):
                if j == i:
                    continue
                self.logger.debug("sudo route del -host {} gw {}".format(
                    self.nodes[j][0], self.nodes[(i + 1) % (self.num_nodes)][0]))
                if not self.testing:
                    self.connections[i].send_command("sudo route del -host {} gw {}".format(
                        self.nodes[j][0], self.nodes[(i + 1) % (self.num_nodes)][0]))

    def configure_star_topology(self, center, remove=False):
        """Configures the cluster's network topology as a star.

        The specified center node is configured as the star's center point
        and is connected to every other node in a single hop.
        All the other nodes have to first send their packets to the center node
        where they are forwarded to the destination.

        Arguments:
            center {integer} -- The center node's index.
            remove {boolean} -- Remove the configuration (default: {False})
        """

        act = "add"
        if remove:
            act = "del"
        for i in range(self.num_nodes):
            self.logger.debug("Node{}:".format(i + 1))
            if i == center:
                self.logger.debug(
                    "Configuring node {} as center of the star topology.".format(i))
                for j in range(0, self.num_nodes):
                    if j == i:
                        continue
                    self.logger.debug("sudo route {} -host {} gw {}".format(
                        act, self.nodes[j][0], self.nodes[j][0]))
                    if not self.testing:
                        self.connections[i].send_command("sudo route {} -host {} gw {}".format(
                            act, self.nodes[j][0], self.nodes[j][0]))
            else:
                for j in range(0, self.num_nodes):
                    if j == i:
                        continue
                    self.logger.debug("sudo route {} -host {} gw {}".format(
                        act, self.nodes[j][0], self.nodes[center][0]))
                    if not self.testing:
                        self.connections[i].send_command("sudo route {} -host {} gw {}".format(
                            act, self.nodes[j][0], self.nodes[center][0]))

    def configure_tree_topology(self, root, degree=2, remove=False):
        """Configures the cluster's network topology as a tree.

        The tree consists of the specified root node and the nodes,
        which build the subtrees. The childrens are incrementally chosen,
        in other words, sequentially as specified in the config file.

        Arguments:
            root {integer} -- The tree's root node.

        Keyword Arguments:
            degree {integer} -- The maximum number of children (default: {2})
            remove {boolean} -- Remove the configuration (default: {False})
        """

        act = "add"
        if remove:
            act = "del"

        tree = Tree()
        tree.create_node(self.nodes[root][0], root)
        last_node = root
        for i in range(self.num_nodes):
            if i == root:
                continue
            if len(tree.children(last_node)) < degree:
                tree.create_node(self.nodes[i][0], i, last_node)
            elif last_node == root and root != 0:
                last_node = 0
                tree.create_node(self.nodes[i][0], i, last_node)
            elif last_node + 1 == root:
                last_node += 2
                tree.create_node(self.nodes[i][0], i, last_node)
            else:
                last_node += 1
                tree.create_node(self.nodes[i][0], i, last_node)

        self.logger.info("The following tree will be configured:")
        tree.show()

        for i in range(self.num_nodes):
            self.logger.debug("Node{}:".format(i + 1))
            subtree = tree.subtree(i)
            for j in range(self.num_nodes):
                if i == j:
                    continue
                if subtree.contains(j):
                    children = tree.children(i)
                    for child in children:
                        if child.identifier == j or tree.is_ancestor(child.identifier, j):
                            self.logger.debug("sudo route {} -host {} gw {}".format(
                                act, self.nodes[j][0], self.nodes[child.identifier][0]))
                            if not self.testing:
                                self.connections[i].send_command("sudo route {} -host {} gw {}".format(
                                    act, self.nodes[j][0], self.nodes[child.identifier][0]))
                            break
                elif tree.parent(i) != None:
                    self.logger.debug("sudo route {} -host {} gw {}".format(
                        act, self.nodes[j][0], self.nodes[tree.parent(i).identifier][0]))
                    if not self.testing:
                        self.connections[i].send_command("sudo route {} -host {} gw {}".format(
                            act, self.nodes[j][0], self.nodes[tree.parent(i).identifier][0]))
