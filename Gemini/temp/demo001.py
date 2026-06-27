from http import client
from typing import overload

from google import genai
from dotenv import load_dotenv
import os
import time

if load_dotenv(overload=True):
    pass

api_key = os.getenv("API_KEY")

print(f"API Key: {api_key}")
    


#client = genai.Client(
#)