from krita import *

def triggerPlugin():
    Krita.instance().action("python_scripter").trigger()