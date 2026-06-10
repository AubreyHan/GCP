import os
from collections import defaultdict
from google import genai
from google.genai import types

# =====================================================================
# 终极多模态 Token 用量统计标杆程序
# 原生支持全模态动态归类：TEXT（文本）、IMAGE（图片）、AUDIO（音频）、VIDEO（视频）
# =====================================================================

client = genai.Client(
    project="cloud-llm-preview4",
    location="us",
    vertexai=True,
    http_options={"base_url": "https://us-central1-aiplatform.googleapis.com"},
)

MODEL_ALIAS_MAP = {
    "nano banana2": "gemini-3.1-flash-image",
}

input_model = "nano banana2"
actual_model = MODEL_ALIAS_MAP.get(input_model, input_model)
prompt = "请给我生成/画一张黄色的香蕉图片"

print(f"正在使用机型代号 [{input_model}] (底层映射为 API Endpoint: [{actual_model}]) 发起图像生成请求...")

response = client.models.generate_content(
    model=actual_model,
    contents=prompt,
)

usage = response.usage_metadata if response else None

print("-" * 55)
print(f"【Model】: {input_model} (映射为: {actual_model}) @ us")
print(f"【Prompt】: {prompt}")
print(f"【Response 简述】: 成功获取多模态交错输出响应")
print("-" * 55)

if usage:
    print(f"【Token 消耗细化统计报告】")
    
    p_cnt = getattr(usage, "prompt_token_count", 0) or 0
    c_cnt = getattr(usage, "candidates_token_count", 0) or 0
    t_cnt = getattr(usage, "total_token_count", 0) or 0
    cache_cnt = getattr(usage, "cached_content_token_count", 0) or 0
    thought_cnt = getattr(usage, "thoughts_token_count", 0) or 0
    
    def get_mod_str(details_list):
        if not details_list:
            return ""
        mod_map = defaultdict(int)
        for d in details_list:
            m_name = getattr(d.modality, "name", str(d.modality)).split(".")[-1]
            mod_map[m_name] += (d.token_count or 0)
        return "\n".join([f"      * 模态 [{m.upper()}] : {cnt}" for m, cnt in mod_map.items()])

    # 1. Input / Prompt
    print(f"  - Prompt Tokens (输入层总计)     : {p_cnt}")
    p_mods = get_mod_str(getattr(usage, "prompt_tokens_details", []))
    if p_mods:
        print(p_mods)
    print("")

    # 2. Output / Candidate
    print(f"  - Candidate Tokens (输出层总计)  : {c_cnt}")
    c_mods = get_mod_str(getattr(usage, "candidates_tokens_details", []))
    if c_mods:
        print(c_mods)
    print("")

    # 3. Cache
    print(f"  - Cached Content Tokens (缓存命中): {cache_cnt}")
    cache_mods = get_mod_str(getattr(usage, "cache_tokens_details", []))
    if cache_mods:
        print(cache_mods)
    print("")

    # 4. Thoughts
    if thought_cnt:
        print(f"  - Thoughts Tokens (思考推理过程): {thought_cnt}")
        print("")

    # 5. Total 压轴
    print(f"  ========================================")
    print(f"  - Total Tokens (总计消耗)        : {t_cnt}")

else:
    print("【Token 消耗】: 无 usage_metadata 数据")
print("-" * 55)
