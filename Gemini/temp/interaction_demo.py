from google import genai
from google.genai import types
from google.genai.types import HttpOptions

from dotenv import load_dotenv
import os

from pydantic import config

if load_dotenv(override=True):
  pass

api_key = os.environ.get("API_KEY")


client = genai.Client(
  enterprise=True,
  api_key=api_keyclear
  
)

model = "gemini-3.5-flash"

contents = [
  types.Content(
    role="user",
    parts=[
      types.Part.from_text(text="""hello""")
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
  thinking_config=types.ThinkingConfig(
    thinking_level="MEDIUM",
  ),
)

resopnse_turn01 = client.interactions.create(
  model=model,
  #generation_config=generate_content_config,
  input="who are you"
)

print(resopnse_turn01)


