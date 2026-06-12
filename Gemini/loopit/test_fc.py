from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
from loopit import user_prompt, system_instruction, tools_definition

load_dotenv(override=True)

client = genai.Client(
    project="cloud-llm-preview4",
    location="global",
    vertexai=True,
    http_options=types.HttpOptions(
        base_url="https://aiplatform.googleapis.com/v1",
    ),
)

config = types.GenerateContentConfig(
    system_instruction=system_instruction,
    temperature=1.0,
    thinking_config=types.ThinkingConfig(thinking_level="HIGH"),
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
        )
    ),
)

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=user_prompt,
        config=config
    )

    print("Dump:")
    if hasattr(response, 'model_dump_json'):
        print(response.model_dump_json(indent=2))
    else:
        print(response)
        
    fn_calls = []
    if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if getattr(part, 'function_call', None):
                fn_calls.append(part.function_call.name)
    print("Extracted fn_calls:", fn_calls)
except Exception as e:
    print("Error:", e)
