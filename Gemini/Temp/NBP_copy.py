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

import google.genai._common as google_genai_common

original_pretty_repr = google_genai_common._pretty_repr

def custom_pretty_repr(
    obj,
    *,
    indent_level=0,
    indent_delta=2,
    max_len=100,
    max_items=9999,      # Prevent any "<... 1 more items ...>" list/dict truncations
    depth=20,            # Prevent any "<... Max depth ...>" placeholders
    visited=None,
):
    # Dynamically simplify large bytes objects (e.g. image inline_data, thought_signature)
    if isinstance(obj, bytes) and len(obj) > 100:
        return f"b'<bytes: {len(obj)}>'"
        
    return original_pretty_repr(
        obj,
        indent_level=indent_level,
        indent_delta=indent_delta,
        max_len=max_len,
        max_items=max_items,
        depth=depth,
        visited=visited,
    )

# Apply global patch to google-genai representation module
google_genai_common._pretty_repr = custom_pretty_repr

def print_simplified(obj):
    print(obj)

print_simplified(response)

# --- Save inline images to temp_output ---
project_root = "/Users/yuanhancn/Tools/Container/uv/git_repo/GCP"
output_dir = os.path.join(project_root, "temp_output")
os.makedirs(output_dir, exist_ok=True)

image_count = 0
if response.candidates:
    for candidate_idx, candidate in enumerate(response.candidates):
        if candidate.content and candidate.content.parts:
            for part_idx, part in enumerate(candidate.content.parts):
                if part.inline_data and part.inline_data.data:
                    mime_type = part.inline_data.mime_type or "image/jpeg"
                    # Determine file extension based on mime_type
                    if "png" in mime_type:
                        ext = "png"
                    elif "jpeg" in mime_type or "jpg" in mime_type:
                        ext = "jpg"
                    elif "gif" in mime_type:
                        ext = "gif"
                    elif "/" in mime_type:
                        ext = mime_type.split("/")[-1]
                    else:
                        ext = "jpg"
                    
                    image_count += 1
                    filename = f"inline_image_cand{candidate_idx}_part{part_idx}_{image_count}.{ext}"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, "wb") as f:
                        f.write(part.inline_data.data)
                    print(f"\n[Success] Inline data successfully generated and saved as image: {filepath}")

if image_count == 0:
    print("\n[Notice] No inline image data found in the response.")
else:
    print(f"\n[Summary] Total {image_count} images generated and saved to directory: {output_dir}")
