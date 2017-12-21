import subprocess
from pexpect import pxssh
import getpass

print("Starting linux network configuration...")
print("Enabling IP forwarding...")

x = "sysctl -w net.ipv4.ip_forward=1"
node1 = "10.0.1.33"
node2 = "10.0.1.34"
node3 = "10.0.1.35"
node4 = "10.0.1.36"
username = "pi"
password = "raspberry"


print("Testing connection to selected nodes...")

try:
    s = pxssh.pxssh()
    hostname = raw_input('hostname: ')
    username = raw_input('username: ')
    password = getpass.getpass('password: ')
    s.login(hostname, username, password)
    s.sendline('uptime')   # run a command
    s.prompt()             # match the prompt
    print(s.before)        # print everything before the prompt.
    s.sendline('ls -l')
    s.prompt()
    print(s.before)
    s.sendline('df')
    s.prompt()
    print(s.before)
    s.logout()
except pxssh.ExceptionPxssh as e:
    print("pxssh failed on login.")
    print(e)