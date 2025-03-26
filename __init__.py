from krita import *
from . import main
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'libs'))

# This line tells Krita about our plugin
Krita.instance().addExtension(main.AutoBoardingExtension(Krita.instance()))
def createPlugin(parent):
    return main.AutoBoardingExtension(parent)