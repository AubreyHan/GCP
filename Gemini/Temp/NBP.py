from google import genai
from google.genai import client, types
from dotenv import load_dotenv
import os

dotenv_path = "/root/git_repo/GCP/.env"
_ = load_dotenv(dotenv_path=dotenv_path)  

api_key = os.getenv("API_KEY")

client = genai.Client(
    enterprise=True,
    api_key=api_key
)

model = "gemini-3-pro-image"

contents = [
    types.Content(
        role="User",
        types.Part=[
            
        ]
    )
]

