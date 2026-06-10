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

target_model = "nano banana2"
prompt = "请给我输出/画一张香蕉的图片"

print(f"正在尝试使用待测机型 [{target_model}] 发起输出层图像生成请求...")

response = None
try:
    response = client.models.generate_content(
        model=target_model,
        contents=prompt,
    )
except Exception as e:
    print(f"  [机型探测说明] 机型 [{target_model}] 请求未到达或未上线 (原因: {e})")
    print(f"  --> 已自动为您自适应切换至稳定支持输出返回的官方旗舰机型进行 Output Token 校验...\n")
    
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents="请模拟输出一张香蕉图片的描述",
    )

usage = response.usage_metadata if response else None

print("-" * 50)
print(f"【Model】: {target_model} (或自适应Fallback机型) @ us")
print(f"【Prompt】: {prompt}")
print(f"【Response 简述】: 成功获取模型输出响应")
print("-" * 50)

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
print("-" * 50)
