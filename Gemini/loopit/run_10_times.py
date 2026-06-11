import os
import time
from google import genai
from google.genai import types

# Import variables from loopit_mfc_stats
from loopit_mfc_stats import system_instruction, tools_definition, user_prompt

def _load_env_vars():
    for rel_path in ["../../.env/vars", "../.env/vars", ".env/vars"]:
        vars_path = os.path.abspath(os.path.join(os.path.dirname(__file__), rel_path))
        if os.path.exists(vars_path):
            with open(vars_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        parts = line.split("=", 1)
                        if len(parts) == 2:
                            key, val = parts[0].strip(), parts[1].strip()
                            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                                val = val[1:-1]
                            os.environ[key] = val
            break

_load_env_vars()
project_id = os.environ.get("MY_PROJECT_ENV")

client = genai.Client(
    project=project_id,
    location="us",
    vertexai=True,
    http_options={"base_url": "https://us-central1-aiplatform.googleapis.com"},
)

# We will run gemini-3.5-flash with MEDIUM thinking level as specified by user settings
thinking_level = "MEDIUM"
print(f"Running gemini-3.5-flash with thinking level {thinking_level} for 10 times...")

config = types.GenerateContentConfig(
    system_instruction=system_instruction,
    temperature=1.0,
    thinking_config=types.ThinkingConfig(thinking_level=thinking_level),
    tools=tools_definition,
    max_output_tokens=65536,
    tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(
            mode="ANY",
            allowed_function_names=[
                "read",
                "write",
                "edit",
                "shell",
                "generate_assets",
                "finish",
            ],
            stream_function_call_arguments=True,
        )
    ),
)

for i in range(1, 11):
    print(f"\n--- Run {i} ---")
    try:
        response_stream = client.models.generate_content_stream(
            model="gemini-3.5-flash",
            contents=user_prompt,
            config=config
        )
        
        stop_reason = None
        fn_name = None
        
        for chunk in response_stream:
            if chunk.candidates:
                for cand in chunk.candidates:
                    if cand.finish_reason:
                        stop_reason = getattr(cand.finish_reason, 'name', cand.finish_reason)
                    if getattr(cand, 'content', None) and getattr(cand.content, 'parts', None):
                        for part in cand.content.parts:
                            if getattr(part, 'function_call', None):
                                fc = part.function_call
                                if fc.name:
                                    fn_name = fc.name
                                    
        print(f"Stop Reason: {stop_reason}")
        print(f"Function Name: {fn_name}")
    except Exception as e:
        print(f"Error during run {i}: {e}")
    time.sleep(1)
