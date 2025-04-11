from krita import *
from .plugin import AutoboardingPlugin

# Krita plugin entry point
def createPlugin(parent):
    return AutoboardingPlugin(parent)
