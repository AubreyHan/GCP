from google import genai
from dotenv import load_dotenv
from google.genai import types
import os
import time

if load_dotenv(override=True):
    projec_id = os.getenv("PROJECT_ID")
    location = os.getenv("LOCATION")
    base_url = os.getenv("BASE_URL")

client = genai.Client(
    enterprise=True,
    project=projec_id,
    location=location
)

model = "projects/939090871257/locations/global/publishers/google/models/gemini-3-pro-image"

start_time = time.time()

contents = [
    types.Content(
      role="user",
      parts=[
        types.Part.from_text(text="""
            一个苹果
        """)
      ]
    )
  ]

generate_content_config = types.GenerateContentConfig(
  temperature = 1,
  top_p = 0.95,
  max_output_tokens = 65535,
  safety_settings = [types.SafetySetting(
    category="HARM_CATEGORY_HATE_SPEECH",
    threshold="OFF"
  ),types.SafetySetting(
    category="HARM_CATEGORY_DANGEROUS_CONTENT",
    threshold="OFF"
  ),types.SafetySetting(
    category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
    threshold="OFF"
  ),types.SafetySetting(
    category="HARM_CATEGORY_HARASSMENT",
    threshold="OFF"
  )],
  image_config=types.ImageConfig(
      aspect_ratio="1:1",
      image_size="2K",
      output_mime_type="image/png",
    ),
)

response = client.models.generate_content(
    model=model,
    contents=contents,
    config=generate_content_config,
)

import uuid

print("Response generated.")
print(f"Response type: {type(response)}")
print(f"Response candidates: {getattr(response, 'candidates', None)}")

if response.candidates and response.candidates[0].content.parts:
    part = response.candidates[0].content.parts[0]
    print(f"Part type: {type(part)}")
    print(f"Part attributes: {dir(part)}")
    image_bytes = None
    
    if hasattr(part, "inline_data") and part.inline_data:
        image_bytes = part.inline_data.data
        print("Found inline_data.")
    elif hasattr(part, "image") and part.image:
        image_bytes = part.image.image_bytes
        print("Found image.image_bytes.")
    elif hasattr(part, "file_data") and part.file_data:
        print("Found file_data, but don't know how to download it yet.")
        
    if image_bytes:
        random_filename = f"{uuid.uuid4().hex}.png"
        with open(random_filename, "wb") as f:
            f.write(image_bytes)
        print(f"Saved generated image to {random_filename}")
    else:
        print("No image data found in the response. Full part data:", part)
else:
    print("No candidates found in the response. Full response:", response)
