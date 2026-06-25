from google import genai
from google.genai import types
from google.genai.types import HttpOptions

from dotenv import load_dotenv
import os

if load_dotenv(override=True):
  pass

client = genai.Client(
  enterprise=True,
  api_key=os.
)