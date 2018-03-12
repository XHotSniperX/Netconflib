import unittest
import sys
import logging
import socket
sys.path.append('../netconflib')
import netconflib.helper as hlp

class TestGUI(unittest.TestCase):
    """Tests the graphical user interface of Netconfig's sniffing.
    """

    # logger
    logger = None

    @classmethod
    def setUpClass(cls):
        cls.logger = logging.getLogger('test.netconflib.helper')
        cls.logger.info("Starting helper test...")

    def test_my_ip(self):
        """Tests the my ip function.
        """

        my_ip = self.get_my_ip()
        self.assertEqual(my_ip, hlp.get_my_ip())

    def get_my_ip(self):
        """Returns the local IP address of this machine.
        """

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

if __name__ == '__main__':
    LOGGER = logging.getLogger('test')
    LOGGER.setLevel(logging.INFO)
    FH = logging.FileHandler('test.log')
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
