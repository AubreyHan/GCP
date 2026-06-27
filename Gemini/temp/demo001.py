from google import genai
from dotenv import load_dotenv
from google.genai import types
import os
import time

if load_dotenv(override=True):
    projec_id = os.getenv("PROJECT_ID")
    location = os.getenv("LOCATION")
    base_url = os.getenv("BASE_URL")
    api_key = os.getenv("API_KEY")

client = genai.Client(
    enterprise=True,
    api_key=api_key
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
)

response = client.models.generate_content(
    model=model,
    contents=contents,
    config=generate_content_config,
)

print("Response:")


