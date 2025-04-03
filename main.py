from diffusers import DiffusionPipeline

pipeline = DiffusionPipeline.from_pretrained("stable-diffusion-v1-5/stable-diffusion-v1-5", use_safetensors=True)

# print(pipeline)

pipeline.to("cuda")
image = pipeline("An image of elon musk with a cat").images[0]
print(image)
image.save("image.png")