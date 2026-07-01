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
        parts=[
            types.Part.from_text(text='''
            一只小狗在草地上奔跑
            ''')
        ]
    )
]

generate_content_config = types.GenerateContentConfig(
    temperature=1,
    top_p=0.95,
    max_output_tokens=65535,
    response_modalities=["TEXT","Image"],
    image_config=types.ImageConfig(
        aspect_ratio="1:1",
        image_size="2k",
        output_mime_type="image/jpeg"
    )
)


response = client.models.generate_content(
    model=model,
    config=generate_content_config,
    contents=contents
)

print(response)