import urllib.request
import json
import base64
from io import BytesIO
import os

# the server url if run remotely
url = "192.168.23.194:8188"

def genImage(prompt, width=512, height=512):
    # Basic stable diffusion workflow
    workflow = {
        "3": {"inputs": {"width": width, "height": height, "batch_size": 1}, "class_type": "EmptyLatentImage"},
        "4": {"inputs": {"text": prompt, "clip": None}, "class_type": "CLIPTextEncode"},
        "5": {"inputs": {"samples": ["3", 0], "conditioning": ["4", 0], "sampler_name": "euler_ancestral", "steps": 20}, "class_type": "KSampler"},
        "6": {"inputs": {"samples": ["5", 0]}, "class_type": "VAEDecode"},
        "7": {"inputs": {"filename_prefix": "output", "images": ["6", 0]}, "class_type": "SaveImage"}
    }
    
    try:
        # Convert workflow to JSON
        data = json.dumps({"prompt": workflow}).encode('utf-8')
        
        # Send request to ComfyUI
        req = urllib.request.Request(
            url+"/api/prompt", 
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as response:
            prompt_id = json.loads(response.read())["prompt_id"]
        
        # Wait for generation to complete
        while True:
            with urllib.request.urlopen(url+"/api/queue") as response:
                queued = json.loads(response.read())
                if prompt_id not in [x[1] for x in queued.get("queue_running", [])]:
                    break
        
        # Get image result
        with urllib.request.urlopen(url+f"/api/history/{prompt_id}") as response:
            history = json.loads(response.read())
            image_data = history["outputs"]["7"]["images"][0]["data"]
        
        # Get path to saved image
        image_path = os.path.join(os.path.expanduser("~"), "ComfyUI", "output", history["outputs"]["7"]["images"][0]["filename"])
        
        return {"success": True, "message": "Image generated", "path": image_path}
    except Exception as e:
        return {"success": False, "message": str(e), "path": None}