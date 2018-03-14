import unittest
import sys
import os
import logging
import socket
from pathlib import Path
sys.path.append('../netconflib')
import netconflib.helper as hlp
from netconflib.server import Server
from netconflib.constants import Paths

class TestGUI(unittest.TestCase):
    """Tests the server.
    """

    # logger
    logger = None

    @classmethod
    def setUpClass(cls):
        cls.logger = logging.getLogger('test.netconflib.server')
        cls.logger.info("Starting server test...")

    def test_init(self):
        """Tests creation of the server instance.
        """

        my_ip = self.get_my_ip()
        cfg_file = Paths.config_file_test_programfolder
        if os.path.isfile(Paths.config_file_test):
            cfg_file = Paths.config_file_test
        s = Server(10006, configfile=cfg_file)
        server_ip = s.local_address

        self.assertIsNotNone(s)
        self.assertEqual(my_ip, server_ip)

    def get_my_ip(self):
        """Returns the local IP address of this machine.
        """

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

if __name__ == '__main__':
    Path(str(Paths.program_home)).mkdir(parents=True, exist_ok=True)
    LOGGER = logging.getLogger('test')
    LOGGER.setLevel(logging.INFO)
    FH = logging.FileHandler(Paths.log_file_test)
    FH.setLevel(logging.INFO)
    CH = logging.StreamHandler()
    CH.setLevel(logging.INFO)
    FORMATTER = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    FH.setFormatter(FORMATTER)
    CH.setFormatter(FORMATTER)
    LOGGER.addHandler(FH)
    LOGGER.addHandler(CH)
    unittest.main()
