import configparser
import io
import ssh
import commands

# number of nodes
numNodes = 0
# host addresses
nodes = []
# connections to nodes
connections = []
# authentication
username = ""
password = ""

cmds = commands.Commands()

print("Starting linux network configuration...")

# Load the configuration file
config = configparser.ConfigParser()
config.read("../config.ini")

nodes = config.items("hosts")
numNodes = len(nodes)
username = config.get("authentication", "username")
password = config.get("authentication", "password")

print("Testing connection to all specified nodes...")

for node, addr in nodes:
    connections.append(ssh.ssh(addr, username, password))

for c in connections:
    c.sendCommand(cmds.cmd_echo)
