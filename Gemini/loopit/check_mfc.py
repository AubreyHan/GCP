#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
import os
import time
import concurrent.futures
from google import genai
from google.genai import types
from loopit import user_prompt, system_instruction, tools_definition

load_dotenv(override=True)

THINKING_LEVELS = [
    "THINKING_LEVEL_UNSPECIFIED",
    "MINIMAL",
    "LOW",
    "MEDIUM",
    "HIGH",
]

def run_single_request(thinking_level, max_retries=3):
    client = genai.Client(
        project="cloud-llm-preview4",
        location="global",
        vertexai=True,
    )
    
    t_config = (
        types.ThinkingConfig(thinking_level=thinking_level)
        if thinking_level != "THINKING_LEVEL_UNSPECIFIED"
        else None
    )
    
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
    
    for attempt in range(1, max_retries + 1):
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
                        
            is_mfc = len(fn_calls) >= 2
            return {
                "success": True,
                "is_mfc": is_mfc,
                "fn_calls": fn_calls,
                "count": len(fn_calls)
            }
        except Exception as e:
            if attempt == max_retries:
                return {
                    "success": False,
                    "error": str(e)
                }
            time.sleep(2 * attempt)

def run_level(level, num_runs=100, max_workers=10):
    print(f"\n[{level}] 开始运行 {num_runs} 次测试 (并发: {max_workers}) ...")
    t0 = time.time()
    
    completed = 0
    mfc_count = 0
    errors = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(run_single_request, level) for _ in range(num_runs)]
        for future in concurrent.futures.as_completed(futures):
            completed += 1
            res = future.result()
            if res["success"]:
                if res["is_mfc"]:
                    mfc_count += 1
            else:
                errors += 1
                
            if completed % 20 == 0 or completed == num_runs:
                print(f"  -> 进度: {completed}/{num_runs} (MFC 次数: {mfc_count}, 错误: {errors})")
                
    t1 = time.time()
    rate = (mfc_count / num_runs) * 100
    print(f"[{level}] 测试完成! 耗时: {t1-t0:.2f}s | MFC 出现次数: {mfc_count}/{num_runs} ({rate:.1f}%)")
    return {
        "level": level,
        "mfc_count": mfc_count,
        "errors": errors,
        "time": t1 - t0,
        "rate": rate
    }

if __name__ == "__main__":
    print("=" * 60)
    print("      Gemini 3.5 Flash MFC (Multi-Function Calling) 检查")
    print("=" * 60)
    print("模型: gemini-3.5-flash")
    print("单层级运行次数: 100 遍")
    print(f"待测试 Thinking Levels: {THINKING_LEVELS}")
    print("=" * 60)
    
    summary = []
    t_start_all = time.time()
    
    for level in THINKING_LEVELS:
        res = run_level(level, num_runs=100, max_workers=10)
        summary.append(res)
        
    t_end_all = time.time()
    
    print("\n" + "=" * 60)
    print("                       最终统计报告 (按 Thinking Level)")
    print("=" * 60)
    print(f"{'Thinking Level':<28} | {'MFC 次数 / 总遍数':<18} | {'MFC 概率':<10}")
    print("-" * 60)
    for row in summary:
        mfc_str = f"{row['mfc_count']} / 100"
        rate_str = f"{row['rate']:.1f}%"
        print(f"{row['level']:<28} | {mfc_str:<18} | {rate_str:<10}")
    print("=" * 60)
    print(f"总耗时: {t_end_all - t_start_all:.2f}s")
