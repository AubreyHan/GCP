from google import genai
from dotenv import load_dotenv
from google.genai import types
import os
import time

load_dotenv(override=True)
project_id = os.getenv("PROJECT_ID")
location = os.getenv("LOCATION")
base_url = os.getenv("BASE_URL")
api_key = os.getenv("API_KEY")

client = genai.Client(
    enterprise=True,
    api_key=api_key,
)

model = "gemini-3-pro-image"

start_time = time.time()

prompt = "A futuristic city with flying cars at sunset, cyberpunk style, high resolution"

generate_images_config = types.GenerateImagesConfig(
    number_of_images=1,
    output_mime_type="image/jpeg",
    aspect_ratio="1:1"
)

print(f"Generating image with {model}...")
response = client.models.generate_images(
    model=model,
    prompt=prompt,
    config=generate_images_config,
)

end_time = time.time()
print(f"Time taken: {end_time - start_time:.2f} seconds")

for i, generated_image in enumerate(response.generated_images):
    image_path = f"output_{i}.jpg"
    with open(image_path, "wb") as f:
        f.write(generated_image.image.image_bytes)
    print(f"Saved image to {image_path}")
