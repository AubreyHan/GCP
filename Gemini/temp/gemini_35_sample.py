#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gemini 3.5 Flash 综合示例程序
严格遵循 auto-gemini-client 标准初始化流程
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    # 加载环境变量
    load_dotenv(override=True)
    
    project_id = os.environ.get("PROJECT_ID", "cloud-llm-preview4")
    location = os.environ.get("LOCATION", "global")
    base_url = os.environ.get("BASE_URL")
    
    http_opts = types.HttpOptions(base_url=base_url) if base_url else None

    # 严格遵循 auto-gemini-client 规范初始化 Client
    client = genai.Client(
        project=project_id,
        location=location,
        http_options=http_opts,
        vertexai=True,
    )
    
    model_name = "gemini-3.5-flash"
    prompt = "请介绍一下 Gemini 3.5 Flash 模型的核心优势，并给出 3 个适用场景。"
    
    config = types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=2048,
        system_instruction="你是一位资深的 AI 架构师，回答要求清晰条理，重点突出。",
    )
    
    print(f"Initializing GenAI Client [Project: {project_id}, Location: {location}] ...")
    print(f"Sending request to [{model_name}] ...\n")
    print("-" * 50)
    
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=config,
        )
        print(response.text)
        print("-" * 50)
        if response.usage_metadata:
            print(f"Token 用量: Prompt={response.usage_metadata.prompt_token_count}, "
                  f"Candidates={response.usage_metadata.candidates_token_count}, "
                  f"Total={response.usage_metadata.total_token_count}")
    except Exception as e:
        print(f"Generation failed: {e}")

if __name__ == "__main__":
    main()
