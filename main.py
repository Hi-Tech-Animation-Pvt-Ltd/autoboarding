from krita import *
from PyQt5.QtWidgets import QMessageBox

# importing my locally built modules
from . import ui

class AutoBoardingExtension(Extension):

    def __init__(self, parent = None):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        # putting our extenstion to be accessible throught tools/scripts
        action = window.createAction("autoboarding", "AutoBoarding", "tools/scripts")
        action.triggered.connect(self.showDialog)

    def showDialog(self):
        # krita's main window
        ui.show_autoboarding_dialog()
