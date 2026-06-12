import concurrent.futures
import time
from google import genai
from google.genai import types
from loopit import client, user_prompt, system_instruction, tools_definition

print("Testing concurrent execution (10 workers, 20 requests)...")

def run_request(idx):
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=1.0,
        thinking_config=types.ThinkingConfig(thinking_level="MINIMAL"),
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
        t0 = time.time()
        res = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=user_prompt,
            config=config
        )
        t1 = time.time()
        fn_calls = []
        if res.candidates and res.candidates[0].content and res.candidates[0].content.parts:
            for p in res.candidates[0].content.parts:
                if getattr(p, 'function_call', None):
                    fn_calls.append(p.function_call.name)
        return {"status": "success", "count": len(fn_calls), "fn_calls": fn_calls, "time": t1 - t0}
    except Exception as e:
        return {"status": "error", "error": str(e)}

t_start = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(run_request, range(20)))
t_end = time.time()

successes = [r for r in results if r["status"] == "success"]
errors = [r for r in results if r["status"] == "error"]

print(f"Total Time: {t_end - t_start:.2f}s")
print(f"Success: {len(successes)}, Error: {len(errors)}")
if errors:
    print(f"Sample error: {errors[0]}")
