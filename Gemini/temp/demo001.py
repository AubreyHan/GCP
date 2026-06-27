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

model = "gemini-3.1-flash-lite"

start_time = time.time()

contents = "how tall is the eiffel tower?"


