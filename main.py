import logging
import argparse
from netconflib.netconf import NetConf
from sniffer import Sniffer

class Main(object):
    """Main class.
    """

    def run(self):
        """Runs the configurator.
        """

        # parser
        parser = argparse.ArgumentParser(description='Network configurator.')
        parser.add_argument('-verbose', action='store_true',
                            help='print debug information (default: only info and error)')
        parser.add_argument('-sniff', action='store_true',
                            help='print packets on the network interface')
        parser.add_argument('--version', action='version', version='Netconf  v0.2')
        args = parser.parse_args()

        # logging configuration
        logger = logging.getLogger('app')
        logger.setLevel(logging.DEBUG)
        f_handler = logging.FileHandler('app.log')
        f_handler.setLevel(logging.DEBUG)
        c_handler = logging.StreamHandler()
        if args.verbose:
            c_handler.setLevel(logging.DEBUG)
        else:
            c_handler.setLevel(logging.ERROR)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(formatter)
        c_handler.setFormatter(formatter)
        logger.addHandler(f_handler)
        logger.addHandler(c_handler)

        if args.sniff:
            sniffer = Sniffer()
            sniffer.sniff_ethernet()
        else:
            ncl = NetConf("config.ini")
            # ncl.enable_ip_forwarding()
            # ncl.configure_ring_topology()
            # ncl.update_hosts_file()
            # ncl.configure_star_topology(0)
            # ncl.configure_tree_topology(3, 1, True)
            ncl.open_shells()

if __name__ == '__main__':
    Main().run()
