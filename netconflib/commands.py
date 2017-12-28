"""This module encapsulates constant shell commands."""

class Commands:
    """This class holds many shell commands.

    You can use this class to access many constant shell commands.
    """

    cmd_echo = "echo hello"
    cmd_ipforward = "sysctl -w net.ipv4.ip_forward=1"
