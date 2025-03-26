from krita import *
from . import main

# This line tells Krita about our plugin
Krita.instance().addExtension(main.AutoBoardingExtension(Krita.instance()))
def createPlugin(parent):
    return main.AutoBoardingExtension(parent)