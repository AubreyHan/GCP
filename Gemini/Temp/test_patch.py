import google.genai._common as google_genai_common

original_pretty_repr = google_genai_common._pretty_repr

def custom_pretty_repr(
    obj,
    *,
    indent_level=0,
    indent_delta=2,
    max_len=100,
    max_items=9999,
    depth=20,
    visited=None,
):
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

google_genai_common._pretty_repr = custom_pretty_repr

# Now run a test
from google import genai
import os

client = genai.Client(enterprise=True, api_key=os.getenv("API_KEY"))
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Tell me a joke."
)

print("--- Testing print(response) ---")
print(response)
