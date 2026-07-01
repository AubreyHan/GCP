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
        image_size="1k",
        output_mime_type="image/jpeg"
    )
)


response = client.models.generate_content(
    model=model,
    config=generate_content_config,
    contents=contents
)

def print_simplified(obj):
    import copy
    import pydantic
    # Create a deep copy to keep the original response object intact
    cloned = copy.deepcopy(obj)
    
    # Recursive helper to simplify fields in Pydantic models or collections
    def simplify(node):
        if isinstance(node, pydantic.BaseModel):
            for field in list(type(node).model_fields.keys()):
                val = getattr(node, field, None)
                if val is None:
                    continue
                if field == "inline_data":
                    if hasattr(val, "data") and isinstance(val.data, bytes):
                        size = len(val.data)
                        val.data = f"<bytes: {size}>".encode()
                elif isinstance(val, bytes) and len(val) > 100:
                    setattr(node, field, f"<bytes: {len(val)} Richmond>".encode() if False else f"<bytes: {len(val)}>".encode())
                else:
                    simplify(val)
        elif isinstance(node, list):
            for item in node:
                simplify(item)
        elif isinstance(node, dict):
            for k, v in node.items():
                if isinstance(v, bytes) and len(v) > 100:
                    node[k] = f"<bytes: {len(v)}>".encode()
                else:
                    simplify(v)

    simplify(cloned)
    print(cloned)

print_simplified(response)