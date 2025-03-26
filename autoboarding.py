from krita import *
from PyQt5.QtWidgets import *


# this is to show the widget if want to open through the tools/script
def showwin():
    QMessageBox.information(QWidget(), "AutoBoarding", "It works yippee!")

class AutoBoardingDocker(DockWidget):

    def __init__(self, parent = ...):
        super().__init__()

        # Setting up the docker widget
        self.setWindowTitle("AutoBoarding")
        mainWidget = QWidget(self)      # <---- initialising the docker mainWidget
        self.setWidget(mainWidget)      # <---- setting up  the docker

        # example button =====================================================================
        exampleButton = QPushButton("show popup", mainWidget)
        exampleButton.clicked.connect(self.popup)

        mainWidget.setLayout(QVBoxLayout())
        mainWidget.layout().addWidget(exampleButton)

    def popup(self):
        QMessageBox.information(QWidget(), "AutoBoarding", "yippeee!")

    def canvasChanged(self, canvas):
        pass


# ----- docker widget code -----
Krita.instance().addDockWidgetFactory(DockWidgetFactory("autoboarding", DockWidgetFactoryBase.DockRight, AutoBoardingDocker))