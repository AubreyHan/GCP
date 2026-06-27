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

contents = [
    types.Content(
      role="user",
      parts=[
        types.Part.from_text(text="""
            逻辑推理题 - 三神
            有代号 A, B, C 的三位神祇，
            只知祂们名为“真实、虚谎、任性”，
            但不知哪个代号属哪个名字。
            真实之神只说真话，虚谎之神只说假话，
            而任性之神会随意说真话或假话。
            你的任务需找出 A, B, C 的身份，
            但每次只能向一位神祇发问。
            神祇们都懂得你的语言，
            但只会用祂们的语言回答 "da" 或 "ja"。
            这两种回答，一个解“是”，一个解“否”，
            但你不知道哪个回答哪个意思。
            你该如何确定每个神的身份？
        """)
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
)

respnse = 

