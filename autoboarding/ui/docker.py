import logging
from typing import Optional
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QSpinBox, QDoubleSpinBox,
    QComboBox, QProgressBar, QFrame
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QImage
from krita import *

from ..backend.api import StableDiffusionAPI
from ..config import Config

class AutoboardingDocker(DockWidget):
    """Main docker panel for the Autoboarding plugin."""
    
    TITLE = "Autoboarding"
    
    def __init__(self, api: StableDiffusionAPI, config: Config):
        """Initialize the docker panel.
        
        Args:
            api: StableDiffusionAPI instance
            config: Plugin configuration instance
        """
        super().__init__()
        self.api = api
        self.config = config
        self.logger = logging.getLogger('Autoboarding.Docker')
        
        # Set up the UI
        self.setWindowTitle(self.TITLE)
        self.main_widget = QWidget()
        self.setWidget(self.main_widget)
        self._setup_ui()
        self._connect_signals()
        
        # Initialize state
        self.current_canvas = None
        self.preview_image = None
    
    def _setup_ui(self):
        """Create and arrange UI components."""
        layout = QVBoxLayout()
        self.main_widget.setLayout(layout)
        
        # Status indicator
        status_layout = QHBoxLayout()
        self.status_label = QLabel("⚫ Not Connected")
        self.check_connection_btn = QPushButton("Check Connection")
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.check_connection_btn)
        layout.addLayout(status_layout)
        
        # Prompt input
        layout.addWidget(QLabel("Prompt:"))
        self.prompt_input = QTextEdit()
        self.prompt_input.setMaximumHeight(60)
        layout.addWidget(self.prompt_input)
        
        # Negative prompt
        layout.addWidget(QLabel("Negative Prompt:"))
        self.negative_prompt_input = QTextEdit()
        self.negative_prompt_input.setMaximumHeight(40)
        layout.addWidget(self.negative_prompt_input)
        
        # Generation parameters
        params_layout = QHBoxLayout()
        
        # Width & Height
        size_layout = QVBoxLayout()
        self.width_input = QSpinBox()
        self.width_input.setRange(64, 2048)
        self.width_input.setValue(self.config.default_width)
        self.height_input = QSpinBox()
        self.height_input.setRange(64, 2048)
        self.height_input.setValue(self.config.default_height)
        size_layout.addWidget(QLabel("Width:"))
        size_layout.addWidget(self.width_input)
        size_layout.addWidget(QLabel("Height:"))
        size_layout.addWidget(self.height_input)
        params_layout.addLayout(size_layout)
        
        # Steps & CFG
        steps_cfg_layout = QVBoxLayout()
        self.steps_input = QSpinBox()
        self.steps_input.setRange(1, 150)
        self.steps_input.setValue(self.config.default_steps)
        self.cfg_input = QDoubleSpinBox()
        self.cfg_input.setRange(1.0, 30.0)
        self.cfg_input.setValue(self.config.default_cfg_scale)
        steps_cfg_layout.addWidget(QLabel("Steps:"))
        steps_cfg_layout.addWidget(self.steps_input)
        steps_cfg_layout.addWidget(QLabel("CFG Scale:"))
        steps_cfg_layout.addWidget(self.cfg_input)
        params_layout.addLayout(steps_cfg_layout)
        
        # Sampler selection
        sampler_layout = QVBoxLayout()
        self.sampler_input = QComboBox()
        self.sampler_input.addItems([
            "Euler a", "Euler", "LMS", "Heun", "DPM2",
            "DPM2 a", "DPM++ 2S a", "DPM++ 2M"
        ])
        self.sampler_input.setCurrentText(self.config.default_sampler)
        sampler_layout.addWidget(QLabel("Sampler:"))
        sampler_layout.addWidget(self.sampler_input)
        params_layout.addLayout(sampler_layout)
        
        layout.addLayout(params_layout)
        
        # Generate button & progress
        gen_layout = QHBoxLayout()
        self.generate_btn = QPushButton("Generate")
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()
        gen_layout.addWidget(self.generate_btn)
        gen_layout.addWidget(self.progress_bar)
        layout.addLayout(gen_layout)
        
        # Preview area
        self.preview_label = QLabel()
        self.preview_label.setMinimumSize(QSize(256, 256))
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        layout.addWidget(self.preview_label)
        
        # Insert button
        self.insert_btn = QPushButton("Insert into Document")
        self.insert_btn.setEnabled(False)
        layout.addWidget(self.insert_btn)
    
    def _connect_signals(self):
        """Connect UI signals to handlers."""
        self.check_connection_btn.clicked.connect(self._check_connection)
        self.generate_btn.clicked.connect(self._generate)
        self.insert_btn.clicked.connect(self._insert_into_document)
        
        # Connect API signals
        self.api.generation_started.connect(self._on_generation_started)
        self.api.generation_progress.connect(self._on_generation_progress)
        self.api.generation_complete.connect(self._on_generation_complete)
        self.api.generation_failed.connect(self._on_generation_failed)
    
    def _check_connection(self):
        """Check backend API connection."""
        status = self.api.check_connection()
        if status["connected"]:
            self.status_label.setText(f"🟢 Connected ({status['api_type']})")
            self.generate_btn.setEnabled(True)
        else:
            self.status_label.setText(f"🔴 Error: {status['error']}")
            self.generate_btn.setEnabled(False)
    
    def _generate(self):
        """Start image generation."""
        self.api.generate_image(
            prompt=self.prompt_input.toPlainText(),
            negative_prompt=self.negative_prompt_input.toPlainText(),
            width=self.width_input.value(),
            height=self.height_input.value(),
            steps=self.steps_input.value(),
            cfg_scale=self.cfg_input.value(),
            sampler=self.sampler_input.currentText()
        )
    
    def _on_generation_started(self):
        """Handle generation start."""
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        self.generate_btn.setEnabled(False)
        self.insert_btn.setEnabled(False)
    
    def _on_generation_progress(self, progress: int):
        """Handle generation progress update."""
        self.progress_bar.setValue(progress)
    
    def _on_generation_complete(self, image):
        """Handle generation completion."""
        self.preview_image = image
        self._update_preview()
        self.progress_bar.hide()
        self.generate_btn.setEnabled(True)
        self.insert_btn.setEnabled(True)
    
    def _on_generation_failed(self, error: str):
        """Handle generation failure."""
        self.progress_bar.hide()
        self.generate_btn.setEnabled(True)
        self.status_label.setText(f"🔴 Error: {error}")
    
    def _update_preview(self):
        """Update the preview image display."""
        if self.preview_image:
            # Convert PIL Image to QPixmap
            data = self.preview_image.convert("RGBA").tobytes("raw", "RGBA")
            qimg = QImage(data, self.preview_image.width, self.preview_image.height,
                         QImage.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qimg)
            
            # Scale to fit preview area while maintaining aspect ratio
            scaled = pixmap.scaled(
                self.preview_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.preview_label.setPixmap(scaled)
    
    def _insert_into_document(self):
        """Insert the generated image into the Krita document."""
        if not self.preview_image or not self.current_canvas:
            return
            
        document = self.current_canvas.document()
        if document:
            # Create a new layer
            root = document.rootNode()
            layer = document.createNode("AI Generated", "paintlayer")
            root.addChildNode(layer, None)
            
            # Convert PIL image to bytes
            byte_array = QByteArray()
            buffer = QBuffer(byte_array)
            buffer.open(QIODevice.WriteOnly)
            
            # Save as PNG
            qimg = QImage(
                self.preview_image.tobytes("raw", "RGBA"),
                self.preview_image.width,
                self.preview_image.height,
                QImage.Format_RGBA8888
            )
            qimg.save(buffer, "PNG")
            
            # Insert into layer
            layer.setPixelData(bytes(byte_array), 0, 0, 
                             self.preview_image.width,
                             self.preview_image.height)
            document.refreshProjection()
    
    def canvas_changed(self, canvas):
        """Handle canvas change events."""
        self.current_canvas = canvas
