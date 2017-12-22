import ssh

print("Starting linux network configuration...")

cmd_ipforward = "sysctl -w net.ipv4.ip_forward=1"
node1 = "10.0.1.33"
node2 = "10.0.1.34"
node3 = "10.0.1.35"
node4 = "10.0.1.36"
username = "pi"
password = "raspberry"

i = 1

connection = ssh.ssh(node1, username, password)
connection.sendCommand(cmd_ipforward)