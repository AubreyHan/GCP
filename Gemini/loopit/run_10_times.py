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
    location="global",
    vertexai=True,
)

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

i = 1
while i <= 10:
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
        i += 1
        time.sleep(2)
    except Exception as e:
        err_msg = str(e)
        if "429" in err_msg or "Resource exhausted" in err_msg:
            print(f"Got 429 Resource Exhausted. Sleeping 15 seconds before retrying run {i}...")
            time.sleep(15)
        else:
            print(f"Error during run {i}: {e}")
            i += 1
            time.sleep(2)
