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
        except Exception as ex:
            print(ex)
            print("connection test failed. Exiting...")
            exit(1)
        print("Successfully connected to all nodes.")

    def enableIPForwarding(self):
        for c in self.connections:
            c.sendCommand(self.cmds.cmd_echo)

    def configureRingTopology(self, parameter_list):
        pass
