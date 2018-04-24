import logging
import argparse
from .netconf import NetConf
from .server import Server
from .client import Client
from pathlib import Path
from .helper import get_my_ip
from .constants import Commands
from .constants import Paths

def init_parser():
    """Initializes the argument parser.

    Returns:
            args -- The parsed arguments.
    """

    parser = argparse.ArgumentParser(description='Network configurator.',
                                    formatter_class=argparse.RawTextHelpFormatter)
    config_help = '''The absolute path to the config.ini file.
The configuration file indicates the nodes' ip addresses (hosts)
and the authentication that is required to login to them.

A sample config.ini file would be:
                        
[hosts]
node1=10.0.1.33
node2=10.0.1.34
node3=10.0.1.35
node4=10.0.1.36

[authentication]
username=pi
password=raspberry

[visualization]
server_address=automatic

[settings]
testing=no
'''
    parser.add_argument("-config", nargs=1, type=str, metavar=('CONFIG-PATH'),
                        help=config_help)
    parser.add_argument('-server', nargs='?', const=10000, type=int, metavar=('PORT'),
                        help='Start server for client sniffing (sepcify port with -server <PORT>, defualt: 10000).')
    parser.add_argument('-client', nargs='?', const=10000, type=int, metavar=('PORT'),
                        help='Start clients for sniffing (sepcify port with -client <PORT>, defualt: 10000).')
    parser.add_argument('-sniff', nargs=2, type=str, metavar=('SERVER-ADDRESS', 'PORT'),
                        help='Start sniffing on the network interface (-sniff <server address> <port>).')
    parser.add_argument('-shells', action='store_true',
                        help='Open shells to all cluster nodes.')
    parser.add_argument('-shell', nargs=1, type=int, metavar=('NODE-ID'),
                        help="Open shell to cluster node with id.")
    parser.add_argument('-ipforward', action='store_true',
                        help="Enable ip forwarding on every node of the cluster.")
    parser.add_argument('-sshsetup', action='store_true',
                        help="Setup ssh keys for internal communication on the cluster.")
    parser.add_argument('-updatehosts', action='store_true',
                        help="Updates the hosts file of every node of the cluster.")
    parser.add_argument('-ring', action='store_true',
                        help="Configure the cluster's network topology as a ring.")
    parser.add_argument('-removering', action='store_true',
                        help="Remove the cluster's ring network topology. Use only after having configured a ring.")
    parser.add_argument('-star', nargs='?', const=0, type=int, metavar=('CENTER'),
                        help="Configure the cluster's network topology as a star (-star <center>). Default center = 0.")
    parser.add_argument('-removestar', nargs='?', const=0, type=int, metavar=('CENTER'),
                        help="Remove the cluster's star network topology (-removestar <center>). Default center = 0.")
    parser.add_argument('-tree', nargs=2, type=int, metavar=('ROOT', 'DEGREE'),
                        help="Configure the cluster's network topology as a tree (-tree <root> <degree>).")
    parser.add_argument('-removetree', nargs=2, type=int, metavar=('ROOT', 'DEGREE'),
                        help="Remove the cluster's tree network topology (-removetree <root> <degree>).")
    parser.add_argument('--verbose', action='store_true',
                        help='Print debug information (default: only info and error).')
    parser.add_argument('--version', action='version', version='Netconf  v1.0.3')

    return parser.parse_args()

def configure_logging(args):
    """Configures the logger.
    
    Arguments:
        args {args} -- The parsed arguments from cli.
    """

    # logging configuration
    logger = logging.getLogger('app')
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    f_handler = logging.FileHandler(Paths.log_file)
    f_handler.setLevel(logging.DEBUG)
    c_handler = logging.StreamHandler()
    if args.verbose:
        c_handler.setLevel(logging.DEBUG)
    else:
        c_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
    formatter_complex = logging.Formatter(
        '%(asctime)s - %(threadName)s - %(name)s - %(levelname)s : %(lineno)d - %(message)s')
    f_handler.setFormatter(formatter_complex)
    c_handler.setFormatter(formatter)
    logger.addHandler(f_handler)
    logger.addHandler(c_handler)

def main(args=None):
    """Runs the configurator.
    """

    Path(str(Paths.program_home)).mkdir(parents=True, exist_ok=True)
    args = init_parser()
    configure_logging(args)

    configfile = None
    if args.config is not None:
        if not Path(args.config[0]).is_file():
            logging.error("The specified path is not a file. Exiting...")
            exit(1)
        else:
            configfile = args.config[0]
    if args.server is not None:
        server = Server(args.server, configfile=configfile)
        server.start_server()
    elif args.sniff is not None:
        client = Client((args.sniff[0], int(float(args.sniff[1]))))
        client.start_sniffer()
    else:
        ncl = NetConf(configfile)
        if args.shells:
            ncl.open_shells()
        elif args.shell is not None:
            ncl.open_shell(args.shell[0])
        elif args.ipforward:
            ncl.enable_ip_forwarding()
        elif args.sshsetup:
            ncl.set_up_cluster_ssh()
        elif args.updatehosts:
            ncl.update_hosts_file()
        elif args.ring:
            ncl.configure_ring_topology()
        elif args.removering:
            ncl.configure_ring_topology(remove=True)
        elif args.star is not None:
            center = args.star
            ncl.configure_star_topology(center)
        elif args.removestar is not None:
            center = args.removestar
            ncl.configure_star_topology(center, remove=True)
        elif args.tree is not None:
            root = args.tree[0]
            degree = args.tree[1]
            ncl.configure_tree_topology(root, degree)
        elif args.removetree is not None:
            root = args.removetree[0]
            degree = args.removetree[1]
            ncl.configure_tree_topology(root, degree, remove=True)
        elif args.client is not None:
            logging.info("Starting the clients on the cluster...")
            cmd = Commands.cmd_start_client.format(get_my_ip(), args.client)
            ncl.execute_command_on_all(cmd)

if __name__ == '__main__':
    main()
