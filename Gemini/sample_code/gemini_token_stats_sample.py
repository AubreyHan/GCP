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

# 标准合法的 1x1 像素 PNG 单色图片字节流（用于真实触发大模型图像模态内核）
sample_img_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\rIDATx\x9cc`\xd0\xd2\xc2\x00\x00\x03\x1f\x01\x19\xed\x95\x80\xb7\x00\x00\x00\x00IEND\xaeB`\x82"

print("正在发起多模态（文本 + 图片）混合 Token 评测请求...")

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=[
        "请确认你收到了一张图片，并向我问好：hello",
        types.Part.from_bytes(data=sample_img_bytes, mime_type="image/png"),
    ],
)

usage = response.usage_metadata

print("-" * 50)
print(f"【Model】: gemini-3.5-flash @ us (Multi-Region)")
print(f"【Prompt】: 文本指令 + 1x1像素PNG图片示例")
print(f"【Response】:\n{response.text.strip() if response.text else ""}")
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
