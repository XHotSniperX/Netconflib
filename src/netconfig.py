import subprocess

print("Starting linux network configuration...")
print("Enabling IP forwarding...")

x = "sysctl -w net.ipv4.ip_forward=1"

p = subprocess.Popen(x, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    print line,
retval = p.wait()