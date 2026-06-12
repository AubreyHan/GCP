from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
from loopit import client, user_prompt, system_instruction, tools_definition

levels = ["THINKING_LEVEL_UNSPECIFIED", "MINIMAL", "LOW", "MEDIUM", "HIGH"]

for level in levels:
    print(f"\nTesting thinking_level={level} ...")
    t_config = types.ThinkingConfig(thinking_level=level) if level != "THINKING_LEVEL_UNSPECIFIED" else None
    
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=1.0,
        thinking_config=t_config,
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
        
        fn_calls = []
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if getattr(part, 'function_call', None):
                    fn_calls.append(part.function_call.name)
                    
        print(f"-> Function calls invoked: {fn_calls} (Count: {len(fn_calls)})")
    except Exception as e:
        print(f"-> Error: {e}")
