import unittest
import sys
import logging
import time
from random import randint
from threading import Thread
from queue import Queue
sys.path.append('../netconflib')
from netconflib.gui import GUI

class TestGUI(unittest.TestCase):
    """Tests the graphical user interface of Netconfig's sniffing.
    """

    # logger
    logger = None

    @classmethod
    def setUpClass(cls):
        cls.logger = logging.getLogger('test.netconflib.GUI')
        cls.logger.info("Starting gui test...")

    def test_gui_20_nodes(self):
        """Tests the gui with 20 nodes.
        """

        q = Queue()
        Thread(target=self.worker_thread, args=(q, 20)).start()

        g = GUI(q, 20)
        self.assertTrue(g is not None)
        g.run()

    def worker_thread(self, q, n):
        """Simulates work and calls the gui.
        
        Arguments:
            q {[type]} -- [description]
            n {[type]} -- [description]
        """

        for _ in range(10):
            q.put(randint(1, n))
            time.sleep(1)
        q.put("--QUIT--")

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
