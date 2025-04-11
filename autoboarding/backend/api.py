import logging
import base64
import io
from typing import Optional, Dict, Any
import requests
from PIL import Image
from PyQt5.QtCore import QObject, pyqtSignal

class StableDiffusionAPI(QObject):
    """Interface for communicating with local Stable Diffusion APIs."""
    
    # Signals for progress updates
    generation_started = pyqtSignal()
    generation_progress = pyqtSignal(int)  # Progress percentage
    generation_complete = pyqtSignal(Image.Image)  # Generated PIL Image
    generation_failed = pyqtSignal(str)  # Error message
    
    def __init__(self, config):
        """Initialize the API interface.
        
        Args:
            config: Plugin configuration instance
        """
        super().__init__()
        self.config = config
        self.logger = logging.getLogger('Autoboarding.API')
        self.session = requests.Session()
    
    def generate_image(self, prompt: str, negative_prompt: str = "",
                      width: Optional[int] = None,
                      height: Optional[int] = None,
                      steps: Optional[int] = None,
                      cfg_scale: Optional[float] = None,
                      sampler: Optional[str] = None) -> None:
        """Generate an image using the configured backend.
        
        Args:
            prompt: Text prompt for generation
            negative_prompt: Negative text prompt
            width: Image width (uses default if None)
            height: Image height (uses default if None)
            steps: Number of generation steps (uses default if None)
            cfg_scale: Guidance scale (uses default if None)
            sampler: Sampler name (uses default if None)
        """
        try:
            self.generation_started.emit()
            
            # Use config defaults for missing parameters
            width = width or self.config.default_width
            height = height or self.config.default_height
            steps = steps or self.config.default_steps
            cfg_scale = cfg_scale or self.config.default_cfg_scale
            sampler = sampler or self.config.default_sampler
            
            if self.config.backend_type == "automatic1111":
                result = self._generate_automatic1111(
                    prompt, negative_prompt, width, height,
                    steps, cfg_scale, sampler
                )
            else:  # comfyui
                result = self._generate_comfyui(
                    prompt, negative_prompt, width, height,
                    steps, cfg_scale, sampler
                )
                
            if result:
                self.generation_complete.emit(result)
            
        except Exception as e:
            self.logger.error(f"Generation failed: {e}")
            self.generation_failed.emit(str(e))
    
    def _generate_automatic1111(self, prompt: str, negative_prompt: str,
                              width: int, height: int, steps: int,
                              cfg_scale: float, sampler: str) -> Optional[Image.Image]:
        """Generate using AUTOMATIC1111 API.
        
        Returns:
            PIL Image if successful, None otherwise
        """
        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "sampler_name": sampler,
        }
        
        response = self.session.post(
            f"{self.config.backend_url}/sdapi/v1/txt2img",
            json=payload,
            timeout=self.config.timeout
        )
        response.raise_for_status()
        
        result = response.json()
        image_data = base64.b64decode(result["images"][0])
        return Image.open(io.BytesIO(image_data))
    
    def _generate_comfyui(self, prompt: str, negative_prompt: str,
                         width: int, height: int, steps: int,
                         cfg_scale: float, sampler: str) -> Optional[Image.Image]:
        """Generate using ComfyUI API.
        
        Returns:
            PIL Image if successful, None otherwise
        """
        # TODO: Implement ComfyUI API integration
        raise NotImplementedError("ComfyUI support coming soon")
    
    def check_connection(self) -> Dict[str, Any]:
        """Check backend API connection status.
        
        Returns:
            Dict with connection status information
        """
        try:
            if self.config.backend_type == "automatic1111":
                response = self.session.get(
                    f"{self.config.backend_url}/sdapi/v1/sd-models",
                    timeout=5
                )
                response.raise_for_status()
                return {
                    "connected": True,
                    "models": len(response.json()),
                    "api_type": "automatic1111"
                }
            else:
                # TODO: Implement ComfyUI connection check
                raise NotImplementedError("ComfyUI support coming soon")
        except Exception as e:
            return {
                "connected": False,
                "error": str(e),
                "api_type": self.config.backend_type
            }
