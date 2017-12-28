# -*- coding: utf-8 -*-
"""SSH helper class.

This class gives the ability to remotely execute comands via SSH.
"""

import logging

from paramiko import client


class SSH:
    """This class provides SSH functionality.
    """

    logger = None
    client = None

    def __init__(self, address, username, password):
        self.logger = logging.getLogger('app.netconflib.ssh')
        self.logger.info("Connecting to server {}.".format(address))
        self.client = client.SSHClient()
        self.client.set_missing_host_key_policy(client.AutoAddPolicy())
        self.client.connect(address, username=username,
                            password=password, look_for_keys=False)

    def send_command(self, command):
        """Executes the command on the remote shell and prints the output.

        You can send a shell command to the remote machine and execute it.
        The output will be printed in the console.

        Arguments:
            command {string} -- the SSH command
        """

        if self.client:
            stdin, stdout, stderr = self.client.exec_command(command)
            while not stdout.channel.exit_status_ready():
                # Print data when available
                if stdout.channel.recv_ready():
                    alldata = stdout.channel.recv(1024)
                    prevdata = b"1"
                    while prevdata:
                        prevdata = stdout.channel.recv(1024)
                        alldata += prevdata

                    self.logger.info(str(alldata).encode("utf-8"))
        else:
            self.logger.error("Connection not opened.")
