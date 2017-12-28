import logging
import argparse
from netconflib.netconf import NetConf

# parser
PARSER = argparse.ArgumentParser(description='Network configurator.')
PARSER.add_argument('-verbose', action='store_true',
                    help='print debug information (default: only info and error)')
PARSER.add_argument('--version', action='version', version='Netconf  v0.1')
ARGS = PARSER.parse_args()

# logging configuration
LOGGER = logging.getLogger('app')
LOGGER.setLevel(logging.DEBUG)
FH = logging.FileHandler('app.log')
FH.setLevel(logging.DEBUG)
CH = logging.StreamHandler()
if ARGS.verbose:
    CH.setLevel(logging.DEBUG)
else:
    CH.setLevel(logging.ERROR)
FORMATTER = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
FH.setFormatter(FORMATTER)
CH.setFormatter(FORMATTER)
LOGGER.addHandler(FH)
LOGGER.addHandler(CH)


NCL = NetConf("config.ini")
NCL.enable_ip_forwarding()
# NCL.configure_ring_topology()
NCL.update_hosts_file()
