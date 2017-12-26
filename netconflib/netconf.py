# -*- coding: utf-8 -*-
"""A linux cluster configuration library.

Use this library to simply configure the network topology of a linux cluster.
"""

import configparser
from .ssh import ssh
from .commands import Commands

class NetConf:
    """Configuration library"""
    # number of nodes
    numNodes = 0
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
        print("Starting linux network configuration...")
        # Load the configuration file
        self.config = configparser.ConfigParser()
        self.config.read(configfile)
        self.cmds = Commands()
        self.nodes = self.config.items("hosts")
        self.numNodes = len(self.nodes)
        self.username = self.config.get("authentication", "username")
        self.password = self.config.get("authentication", "password")

        print("Testing connection to all specified nodes...")
        try:
            for node, addr in self.nodes:
                self.connections.append(ssh(addr, self.username, self.password))
                print(node, addr)
        except Exception as ex:
            print(ex)
            print("connection test failed. Exiting...")
            exit(1)
        print("Successfully connected to all nodes.")

    def enableIPForwarding(self):
        """Enables ip packet forwarding on every node on the cluster."""
        print("Enabling IP packet forwarding...")
        for c in self.connections:
            c.sendCommand(self.cmds.cmd_echo)

    def updateHostsFile(self):
        """Adds all the ip addresses and host names to etc/hosts file. TODO implement"""
        for i, c in enumerate(self.connections):
            print("Node{}:".format(i+1))
            for j in range(0, self.numNodes):
                if j == i:
                    print("127.0.1.1    {}".format(self.nodes[j][0]))
                else:
                    print("{}   {}".format(self.nodes[j][1], self.nodes[j][0]))

    def configureRingTopology(self):
        """Configures the cluster's network topology as a ring."""
        for i, c in enumerate(self.connections):
            #print("Node{}:".format(i+1))
            for j in range(0, self.numNodes):
                if j == i:
                    continue
                #print("route add -host {} gw {}".format(self.nodes[j][0], self.nodes[(i + 1) % (self.numNodes)][0]))
                c.sendCommand("sudo route add -host {} gw {}".format(self.nodes[j][0], self.nodes[(i + 1) % (self.numNodes)][0]))

    def removeRingTopology(self):
        """Removes the ring netork topology from the cluster."""
        for i, c in enumerate(self.connections):
            #print("Node{}:".format(i+1))
            for j in range(0, self.numNodes):
                if j == i:
                    continue
                #print("route del -host {} gw {}".format(self.nodes[j][0], self.nodes[(i + 1) % (self.numNodes)][0]))
                c.sendCommand("sudo route del -host {} gw {}".format(self.nodes[j][0], self.nodes[(i + 1) % (self.numNodes)][0]))
