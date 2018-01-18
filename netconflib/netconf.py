# -*- coding: utf-8 -*-
"""A linux cluster configuration library.

Use this library to conveniently configure the network topology of a linux cluster.
"""

import configparser
import logging
from treelib import Tree
from paramiko import BadHostKeyException
from paramiko import AuthenticationException
from paramiko import SSHException
from .ssh import SSH
from .commands import Commands

class NetConf:
    """Configuration library

    This class provides methods to configure the network
    of a Linux cluster.
    """

    # logger
    logger = None

    # topology
    types = None
    topology = None

    cmds = None
    config = None
    testing = False

    def __init__(self, configfile):
        self.logger = logging.getLogger('app.netconflib.NetConf')
        self.logger.info("Starting linux network configuration...")
        self.config = configparser.ConfigParser()
        self.config.read(configfile)
        self.cmds = Commands()
        nodes = self.config.items("hosts")
        num_nodes = len(nodes)
        username = self.config.get("authentication", "username")
        password = self.config.get("authentication", "password")
        self.types = TopologyTypes()
        self.topology = Topology(None, num_nodes, username, password)
        self.topology.clean_up()
        self.topology.add_nodes_from_list(nodes)

        self.testing = self.config.get("settings", "testing")

        if not self.testing:
            self.topology.create_all_connections()

    def enable_ip_forwarding(self):
        """Enables ip packet forwarding on every node on the cluster."""

        self.logger.info("Enabling IP packet forwarding...")
        for node in self.topology.nodes:
            if not self.testing and not node.connection is None:
                node.connection.send_command(self.cmds.cmd_ipforward)

    def update_hosts_file(self):
        """Appends all the ip addresses and host names to etc/hosts file.
        """

        for nodex in self.topology.nodes:
            for nodey in self.topology.nodes:
                if nodex.node_id == nodey.node_id:
                    nodex.add_host("127.0.1.1", nodey.name)
                else:
                    nodex.add_host(nodey.address, nodey.name)

        if not self.testing:
            self.topology.send_all_hosts()

    def configure_ring_topology(self, remove=False):
        """Configures the cluster's network topology as a ring.

        The nodes communicate logically in a ring topology.
        Each node forwards the packet to the next node in the ring
        until the packet arrives at its desired destination.
        The ring is built incrementally as specified in the config file.
        The forwarding direction is always clockwise.

        Keyword Arguments:
            remove {boolean} -- Remove the configuration (default: {False})
        """

        for nodex in self.topology.nodes:
            for nodey in self.topology.nodes:
                if nodex.node_id == nodey.node_id:
                    continue
                nodex.add_forwarding(nodey, self.topology.nodes[(
                    nodex.node_id + 1) % (self.topology.num_nodes)])

        if not self.testing:
            self.topology.send_forwarding_tables(remove)

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

        center_node = self.topology.get_node(center)
        for nodex in self.topology.nodes:
            self.logger.debug("%s:", nodex.name)
            if nodex.node_id == center_node.node_id:
                self.logger.debug(
                    "Configuring %s as center of the star topology.", nodex.name)
                for nodey in self.topology.nodes:
                    if nodex.node_id == nodey.node_id:
                        continue
                    nodex.add_forwarding(nodey, nodey)
            else:
                for nodey in self.topology.nodes:
                    if nodex.node_id == nodey.node_id:
                        continue
                    nodex.add_forwarding(nodey, center_node)

        if not self.testing:
            self.topology.send_forwarding_tables(remove)

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

        tree = Tree()
        root_node = self.topology.get_node(root)
        tree.create_node(root_node.name, root_node.node_id)
        parent_node = root
        for nodex in self.topology.nodes:
            if nodex.node_id == root_node.node_id:
                continue
            if len(tree.children(parent_node)) >= degree:
                if parent_node == root and root != 0:
                    parent_node = 0
                elif parent_node + 1 == root:
                    parent_node += 2
                else:
                    parent_node += 1
            tree.create_node(nodex.name, nodex.node_id, parent_node)

        self.logger.info("The following tree will be configured:")
        tree.show()

        for nodex in self.topology.nodes:
            self.logger.debug("%s:", nodex.name)
            subtree = tree.subtree(nodex.node_id)
            for nodey in self.topology.nodes:
                if nodex.node_id == nodey.node_id:
                    continue
                if subtree.contains(nodey.node_id):
                    children = tree.children(nodex.node_id)
                    for child in children:
                        if (child.identifier == nodey.node_id or
                                tree.is_ancestor(child.identifier, nodey.node_id)):
                            nodex.add_forwarding(
                                nodey, self.topology.get_node(child.identifier))
                            break
                elif tree.parent(nodex.node_id) != None:
                    nodex.add_forwarding(nodey, self.topology.get_node(
                        tree.parent(nodex.node_id).identifier))

        if not self.testing:
            self.topology.send_forwarding_tables(remove)

class Node:
    """This class provides the functionality of a node.
    """

    # logger
    logger = None

    node_id = 0
    name = ""
    address = ""
    connection = None
    forwarding_table = {}
    hosts = {}

    def __init__(self, node_id, name, address):
        self.logger = logging.getLogger('app.netconflib.Node')
        self.node_id = node_id
        self.name = name
        self.address = address

    def add_forwarding(self, dest_node, next_node):
        """Adds a forwarding entry to the table.

        Arguments:
            dest_node {Node} -- The destination node.
            next_node {Node} -- The next node to forward to.
        """

        self.logger.debug("%s: Adding following entry to forwarding table. -host %s gw %s"
                          , self.name, dest_node.name, next_node.name)
        self.forwarding_table.update({dest_node: next_node})

    def add_host(self, address, name):
        """Adds the specified host entry to the node's hosts.

        Arguments:
            address {string} -- The host's address.
            name {string} -- The host's name.
        """

        self.logger.debug("%s: Adding %s %s to hosts.", self.name, address, name)
        self.hosts.update({address: name})

    def send_forwarding_table(self, remove=False):
        """Sends and writes the forwarding entries of this node
        to the corresponding physical node on the cluster.

        Keyword Arguments:
            remove {boolean} -- Remove the configuration (default: {False})
        """

        act = "add"
        if remove:
            act = "del"

        self.logger.debug("%s:", self.name)
        for dest, next_node in self.forwarding_table:
            self.logger.debug(
                "sudo route %s -host %s gw %s", act, dest.name, next_node.name)
            self.connection.send_command(
                "sudo route {} -host {} gw {}".format(act, dest.name, next_node.name))

    def send_hosts(self):
        """Sends and writes the hosts on the node's hosts file.
        """

        for addr, name in self.hosts:
            self.logger.debug("%s: echo '%s    %s' | sudo tee -a /etc/hosts", self.name, addr, name)
            self.connection.send_command(
                "echo '{}    {}' | sudo tee -a /etc/hosts".format(addr, name))

    def create_ssh_connection(self, username, password):
        """Creates an SSH connection to this node.
        The node's address is used. No connection will be created
        if the address is unspecified.

        Arguments:
            username {string} -- SSH username
            password {string} -- SSH password
        """

        if self.address != "":
            self.connection = SSH(self.address, username, password)
        else:
            raise ValueError

class Topology:
    """This class holds the topology of the cluster.
    """

    # logger
    logger = None

    topology_type = None
    num_nodes = 0
    nodes = []
    username = ""
    password = ""

    def __init__(self, topology_type, num_nodes, username, password):
        self.logger = logging.getLogger('app.netconflib.Topology')
        self.topology_type = topology_type
        self.num_nodes = num_nodes
        self.username = username
        self.password = password

    def add_nodes_from_list(self, nodes):
        """Adds new nodes to the topology out of a list of (name, address) tuples.

        Arguments:
            nodes {list} -- List of (name, address) tuples.
        """

        for i, node in enumerate(nodes):
            new_node = Node(i, node[0], node[1])
            self.nodes.append(new_node)

    def clean_up(self):
        """Clears the variables.
        """

        self.nodes.clear()

    def get_node(self, node_id):
        """Returns the node that matches the specified id.

        Arguments:
            node_id {integer} -- The node id.

        Returns:
            Node -- The node object.
        """

        for node in self.nodes:
            if node.node_id == node_id:
                return node

    def create_all_connections(self):
        """Creates connections for every available node in the topology.
        """

        self.logger.info("Establishing connection to all specified nodes...")
        try:
            for node in self.nodes:
                self.logger.debug(
                    "Creating new connection to %s, %s...", node.name, node.address)
                node.create_ssh_connection(self.username, self.password)
        except (ValueError, BadHostKeyException, AuthenticationException, SSHException) as ex:
            self.logger.error(ex)
            self.logger.error("connection failed with %s.", node.name)
        self.logger.info("Connections established.")

    def send_forwarding_tables(self, remove=False):
        """Calls every node object on the cluster to send their forwarding table.

        Keyword Arguments:
            remove {boolean} -- Remove the configuration (default: {False})
        """

        for node in self.nodes:
            node.send_forwarding_table(remove)

    def send_all_hosts(self):
        """Calls every node object on the cluster to send their host entries.
        """

        for node in self.nodes:
            node.send_hosts()

class TopologyTypes:
    """Available topology types.
    """

    TOPOLOGY_RING = "ring"
    TOPOLOGY_STAR = "star"
    TOPOLOGY_TREE = "tree"
