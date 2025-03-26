import requests, base64, io
from PIL import Image

# the server url if run remotely
url = "192.168.23.194:8188"
# editables
width = 512
height = 512

# the Backend class for our AI integration
class aiBackend:
    def __init__(self, url=url):
        self.url = url

    def genPanel(self, prompt, width=width, height=height):
        # Stable diffusion workflow
        workflow = {
            "1": {"inputs": {"width": width, "height": height}, "class_type": "EmptyLatentImage"},
            "2": {"inputs": {"text": prompt}, "class_type": "CLIPTextEncode"},
            "3": {"inputs": {"samples": ["1", 0], "conditioning": ["2", 0]}, "class_type": "KSampler"}
        }

        response = requests.post(f"{self.url}/api/prompt", json={"Prompt": workflow})

        # Get image data
        prompt_id = response.json()["prompt_id"]
        output_data = response.json()[prompt_id]["outputs"]["3"]["images"][0]

        # convert PIL to Image
        image_bytes = base64.b64decode(output_data.split(",")[1])
        return Image.open(io.BytesIO(image_bytes))
    

ai = aiBackend()