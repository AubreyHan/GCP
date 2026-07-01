from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv  # pyright: ignore[reportUnusedExpression]

api_key = os.getenv("API_KEY")
print(api_key)