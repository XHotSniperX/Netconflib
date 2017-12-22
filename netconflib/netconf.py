import ConfigParser
import io
import ssh

# number of nodes
numNodes = 0
# host addresses
nodes = []
# connections to nodes
connections = []
# authentication
username = ""
password = ""

print("Starting linux network configuration...")

# Load the configuration file
with open("../config.ini") as f:
    _config = f.read()
config = ConfigParser.RawConfigParser(allow_no_value=True)
config.readfp(io.BytesIO(_config))

nodes = config.items("hosts")
numNodes = len(nodes)
username = config.get("authentication", "username")
password = config.get("authentication", "password")

print("Testing connection to all specified nodes...")

for node, addr in nodes:
    connections.append(ssh.ssh(addr, username, password))

for c in connections:
    c.sendCommand("echo hello")

cmd_ipforward = "sysctl -w net.ipv4.ip_forward=1"