"""Sniffer class.

This class gives the ability to show network activity.
"""

from scapy.all import *
import logging

class Sniffer(object):
    """This class provides features to display network activity.
    """

    ## Define our Custom Action function
    def custom_action(self, packet):
        """Redefining the packet output.

        Arguments:
            packet {object} -- IP packet.
        """

        self.counter += 1
        return 'Packet #{}: {} ==> {}'.format(self.counter, packet[0][1].src, packet[0][1].dst)

    def __init__(self):
        self.logger = logging.getLogger('app.sniffer')
        self.logger.info("Sniffing on network interface...")
        self.counter = 0

    def sniff_ethernet(self):
        """Sniff only ping (icmp) packets.
        """

        sniff(filter="ip", prn=self.custom_action)
