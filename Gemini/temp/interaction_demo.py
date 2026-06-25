from google import genai
from google.genai import types
from google.genai.types import HttpOptions

from dotenv import load_dotenv
import os

if load_dotenv(override=True):
  pass

api_key = os.environ.get("API_KEY")


client = genai.Client(
  enterprise=True,
  api_key=api_key
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



