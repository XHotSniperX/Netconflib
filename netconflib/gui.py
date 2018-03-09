"""GUI class.

This class is responsible for the gui.
"""

import queue, time
import logging
from appJar import gui

class GUI():
    """This class holds the gui.
    """

    def __init__(self, result_q):
        super(GUI, self).__init__()
        self.logger = logging.getLogger('app.netconflib.gui')
        self.logger.info("Initializing graphical user interface...")
        self.result_q = result_q
        self.counter = 0
        self.app = gui(handleArgs=False)
        self.init_gui()

    def run(self):
        self.app.go()

    def init_gui(self):
        self.app.addLabel("title", "Welcome to appJar")
        self.app.setLabelBg("title", "red")
