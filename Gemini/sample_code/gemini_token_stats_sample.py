from collections import defaultdict
from google import genai

# 按照最新的 multi-region 方式，使用 "us" 作为区域标识；
# 针对本地 DNS 无法解析 mtls.rep 域名的问题，底层重定向至合法的 API 接入点
client = genai.Client(
    project="cloud-llm-preview4",
    location="us",
    vertexai=True,
    http_options={"base_url": "https://us-central1-aiplatform.googleapis.com"},
)

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="hello",
)

usage = response.usage_metadata

print("-" * 50)
print(f"【Model】: gemini-3.5-flash @ us (Multi-Region)")
print(f"【Prompt】: hello")
print(f"【Response】:\n{response.text.strip() if response.text else ''}")
print("-" * 50)

if usage:
    print(f"【Token 消耗细化统计报告】")
    
    p_cnt = getattr(usage, 'prompt_token_count', 0) or 0
    c_cnt = getattr(usage, 'candidates_token_count', 0) or 0
    t_cnt = getattr(usage, 'total_token_count', 0) or 0
    cache_cnt = getattr(usage, 'cached_content_token_count', 0) or 0
    thought_cnt = getattr(usage, 'thoughts_token_count', 0) or 0
    
    def get_mod_str(details_list):
        if not details_list:
            return ""
        mod_map = defaultdict(int)
        for d in details_list:
            m_name = getattr(d.modality, 'name', str(d.modality)).split('.')[-1]
            mod_map[m_name] += (d.token_count or 0)
        return "\n".join([f"      * 模态 [{m.upper()}] : {cnt}" for m, cnt in mod_map.items()])

    # 1. Input / Prompt
    print(f"  - Prompt Tokens (输入层总计)     : {p_cnt}")
    p_mods = get_mod_str(getattr(usage, 'prompt_tokens_details', []))
    if p_mods:
        print(p_mods)
    print("")

    # 2. Output / Candidate
    print(f"  - Candidate Tokens (输出层总计)  : {c_cnt}")
    c_mods = get_mod_str(getattr(usage, 'candidates_tokens_details', []))
    if c_mods:
        print(c_mods)
    print("")

    # 3. Cache
    print(f"  - Cached Content Tokens (缓存命中): {cache_cnt}")
    cache_mods = get_mod_str(getattr(usage, 'cache_tokens_details', []))
    if cache_mods:
        print(cache_mods)
    print("")

    # 4. Thoughts
    if thought_cnt:
        print(f"  - Thoughts Tokens (思考推理过程): {thought_cnt}")
        print("")

    # 5. Total 放在最后压轴
    print(f"  ========================================")
    print(f"  - Total Tokens (总计消耗)        : {t_cnt}")

else:
    print("【Token 消耗】: 无 usage_metadata 数据")
print("-" * 50)

