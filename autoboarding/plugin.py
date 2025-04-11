import logging
from krita import *
from PyQt5.QtWidgets import QWidget

from .ui.docker import AutoboardingDocker
from .config import Config
from .backend.api import StableDiffusionAPI

class AutoboardingPlugin(Extension):
    """Main plugin class for Autoboarding."""
    
    def __init__(self, parent):
        """Initialize the plugin.
        
        Args:
            parent: Parent QObject from Krita
        """
        super().__init__(parent)
        self.docker = None
        self.config = None
        self.api = None
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('Autoboarding')

    def setup(self):
        """Set up the plugin configuration and dependencies."""
        self.config = Config()
        self.api = StableDiffusionAPI(self.config)
        
    def createActions(self, window):
        """Create plugin actions/menu items.
        
        Args:
            window: Krita window instance
        """
        pass  # We'll use the docker interface instead of menu actions

    def canvasChanged(self, canvas):
        """Handle canvas change events.
        
        Args:
            canvas: Current canvas instance
        """
        if self.docker:
            self.docker.canvas_changed(canvas)
            
    def createDocker(self):
        """Create the plugin's docker panel."""
        if not self.docker:
            self.docker = AutoboardingDocker(self.api, self.config)
        return self.docker
