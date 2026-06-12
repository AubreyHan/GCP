#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
import os
import time
import json
import random
import concurrent.futures
from google import genai
from google.genai import types
from loopit import user_prompt, system_instruction, tools_definition  # pyright: ignore[reportImplicitRelativeImport]

load_dotenv(override=True)

THINKING_LEVELS = [
    "MEDIUM",
]

def run_single_request(thinking_level, idx, max_retries=5):
    base_url = os.environ.get("BASE_URL")
    http_opts = types.HttpOptions(base_url=base_url) if base_url else None

    client = genai.Client(
        project=os.environ.get("PROJECT_ID", "cloud-llm-preview4"),
        location=os.environ.get("LOCATION", "global"),
        vertexai=True,
        http_options=http_opts,
    )
    
    t_config = types.ThinkingConfig(thinking_level=thinking_level)
    
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
    
    t0 = time.time()
    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=user_prompt,
                config=config
            )
            t1 = time.time()
            fn_calls = []
            if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if getattr(part, 'function_call', None):
                        fn_calls.append(part.function_call.name)
                        
            is_mfc = len(fn_calls) >= 2
            return {
                "success": True,
                "thinking_level": thinking_level,
                "run_index": idx,
                "is_mfc": is_mfc,
                "function_calls": fn_calls,
                "count": len(fn_calls),
                "duration_s": round(t1 - t0, 2)
            }
        except Exception as e:
            if attempt == max_retries:
                return {
                    "success": False,
                    "thinking_level": thinking_level,
                    "run_index": idx,
                    "error": str(e),
                    "duration_s": round(time.time() - t0, 2)
                }
            time.sleep(1.5 * attempt + random.uniform(0.5, 1.5))

def run_level(level, num_runs=100, max_workers=10):
    print(f"[{level}] 开始并行测试 ({num_runs} 次) ...")
    t0 = time.time()
    
    details = []
    mfc_count = 0
    errors = 0
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(run_single_request, level, idx + 1) for idx in range(num_runs)]
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            details.append(res)
            
            if res.get("success"):
                mfc_flag = "★ MFC" if res.get("is_mfc") else "  SFC"
                fn_list_str = ", ".join(res.get("function_calls", [])) or "None"
                print(f"[{level}] #{res['run_index']:<3} | {mfc_flag} | {res.get('duration_s', 0):>5.2f}s | 函数: [{fn_list_str}]")
                if res.get("is_mfc"):
                    mfc_count += 1
            else:
                errors += 1
                print(f"[{level}] #{res['run_index']:<3} | [ERROR] | {res.get('duration_s', 0):>5.2f}s | 错误: {res.get('error')}")
                
    t1 = time.time()
    rate = (mfc_count / num_runs) * 100
    print(f"[{level}] 完成! 耗时: {t1-t0:.2f}s | MFC 出现次数: {mfc_count}/{num_runs} ({rate:.1f}%)")
    
    details.sort(key=lambda x: x["run_index"])
    return {
        "level": level,
        "mfc_count": mfc_count,
        "errors": errors,
        "time": round(t1 - t0, 2),
        "rate": rate,
        "details": details
    }

def run_once():
    t_start_all = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(THINKING_LEVELS)) as level_executor:
        future_map = {level_executor.submit(run_level, lvl, 100, 10): lvl for lvl in THINKING_LEVELS}
        results = [fut.result() for fut in concurrent.futures.as_completed(future_map)]
        
    t_end_all = time.time()
    
    level_order = {lvl: i for i, lvl in enumerate(THINKING_LEVELS)}
    results.sort(key=lambda r: level_order[r['level']])
    
    # Save the latest detailed results to mfc_details.json
    log_output_path = os.path.join(os.path.dirname(__file__), "mfc_details.json")
    json_data = {
        "model": "gemini-3.5-flash",
        "total_duration_s": round(t_end_all - t_start_all, 2),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "summary": [
            {
                "thinking_level": r["level"],
                "mfc_count": r["mfc_count"],
                "total_runs": 100,
                "mfc_rate": f"{r['rate']:.1f}%",
                "duration_s": r["time"]
            } for r in results
        ],
        "invocation_details": {
            r["level"]: r["details"] for r in results
        }
    }
    
    with open(log_output_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
        
    # Append the summary to mfc_history.log
    history_log_path = os.path.join(os.path.dirname(__file__), "mfc_history.log")
    local_time_str = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(history_log_path, "a", encoding="utf-8") as f_log:
        for r in results:
            log_line = f"[{local_time_str}] Model: gemini-3.5-flash | Level: {r['level']:<8} | MFC Count: {r['mfc_count']}/100 ({r['rate']:.1f}%) | Duration: {r['time']:.2f}s | Errors: {r['errors']}\n"
            f_log.write(log_line)
            
    print("\n" + "=" * 60)
    print("                       最终统计报告 (带实时监控)")
    print("=" * 60)
    print(f"{'Thinking Level':<20} | {'MFC 次数 / 总遍数':<18} | {'MFC 概率':<10}")
    print("-" * 60)
    for row in results:
        mfc_str = f"{row['mfc_count']} / 100"
        rate_str = f"{row['rate']:.1f}%"
        print(f"{row['level']:<20} | {mfc_str:<18} | {rate_str:<10}")
    print("=" * 60)
    print(f"调用明细文件已导出至: {log_output_path}")
    print(f"统计结果已追加至: {history_log_path}")

if __name__ == "__main__":
    INTERVAL_MINUTES = 15
    print("=" * 60)
    print(f"      Gemini 3.5 Flash MFC 终端实时监控 (每 {INTERVAL_MINUTES} 分钟循环运行)")
    print("=" * 60)
    print("模型: gemini-3.5-flash")
    print("运行层级: MEDIUM")
    print(f"运行间隔: {INTERVAL_MINUTES} 分钟")
    print("=" * 60)
    
    try:
        while True:
            start_time = time.time()
            print(f"\n>>> 启动新一轮测试 (时间: {time.strftime('%Y-%m-%d %H:%M:%S')})")
            run_once()
            
            elapsed = time.time() - start_time
            sleep_sec = max(0.0, INTERVAL_MINUTES * 60 - elapsed)
            print(f"\n本轮运行耗时: {elapsed:.2f}s。将等待 {sleep_sec:.2f}s 后启动下一轮...")
            time.sleep(sleep_sec)
    except KeyboardInterrupt:
        print("\n检测到 Ctrl+C，已退出循环测试。")
