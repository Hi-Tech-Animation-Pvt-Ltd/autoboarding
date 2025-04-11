import json
import os
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Config:
    """Configuration class for the Autoboarding plugin."""
    
    # Backend settings
    backend_url: str = "http://127.0.0.1:7860"  # Default A1111 address
    backend_type: str = "automatic1111"  # or "comfyui"
    timeout: int = 30
    
    # Generation settings
    default_width: int = 512
    default_height: int = 512
    default_steps: int = 20
    default_cfg_scale: float = 7.0
    default_sampler: str = "Euler a"
    
    # UI settings
    prompt_history_size: int = 50
    show_advanced: bool = False
    
    def __post_init__(self):
        """Load saved configuration if it exists."""
        self.config_path = Path.home() / ".config" / "krita" / "autoboarding.json"
        self.load()
    
    def load(self) -> None:
        """Load configuration from disk."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                    for key, value in data.items():
                        if hasattr(self, key):
                            setattr(self, key, value)
            except Exception as e:
                print(f"Error loading config: {e}")
    
    def save(self) -> None:
        """Save configuration to disk."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(asdict(self), f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
