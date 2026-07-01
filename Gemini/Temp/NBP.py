from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

dotenv_path = "/root/git_repo/GCP/.env"
load_dotenv(dotenv_path=dotenv_path)  # pyright: ignore[reportUnusedExpression]

api_key = os.getenv("API_KEY")
print(api_key)