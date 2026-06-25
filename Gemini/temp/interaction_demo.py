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
  project="hy-ai-demo",
  location="global"

)

model = "gemini-3.5-flash"
interaction = client.interactions.create(
    model='gemini-3.5-flash',
    input='Tell me a short joke about programming.'
)
print(interaction.outputs[-1].text)