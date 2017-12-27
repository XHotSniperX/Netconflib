import logging
import argparse
from netconflib.netconf import NetConf

# parser
parser = argparse.ArgumentParser(description='Network configurator.')
parser.add_argument('-verbose', action='store_true',
                   help='print debug information (default: only info and error)')
parser.add_argument('--version', action='version', version='Netconf  v0.1')
args = parser.parse_args()

# logging configuration
logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('app.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
if args.verbose:
    ch.setLevel(logging.DEBUG)
else:
    ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


ncl = NetConf("config.ini")
#ncl.enableIPForwarding()
#ncl.configureRingTopology()
ncl.updateHostsFile()
