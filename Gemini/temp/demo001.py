from http import client
from typing import overload

from google import genai
from dotenv import load_dotenv
import os
import time

if load_dotenv(override=True):
    projec_id = os.getenv("PROJECT_ID")
    location = os.getenv("LOCATION")
    base_url = os.getenv("BASE_URL")


print(projec_id, location,base_url)
    


client = genai.Client(
)