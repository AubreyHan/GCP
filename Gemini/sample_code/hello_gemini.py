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
    print(f"【Token 全量与模态细化消耗报告】")
    
    p_cnt = getattr(usage, 'prompt_token_count', 0) or 0
    c_cnt = getattr(usage, 'candidates_token_count', 0) or 0
    t_cnt = getattr(usage, 'total_token_count', 0) or 0
    cache_cnt = getattr(usage, 'cached_content_token_count', 0) or 0
    thought_cnt = getattr(usage, 'thoughts_token_count', 0) or 0
    
    print(f"  [基础总量]")
    print(f"    - Prompt Tokens (总输入)     : {p_cnt}")
    print(f"    - Candidate Tokens (总输出)  : {c_cnt}")
    print(f"    - Total Tokens (总计)        : {t_cnt}")
    print(f"    - Cached Content Tokens (缓存): {cache_cnt}")
    if thought_cnt:
        print(f"    * Thoughts Tokens (思考过程) : {thought_cnt}")
    print("")

    def print_modality_details(label, details_list):
        print(f"  [{label} 按模态细分]")
        if not details_list:
            print("    * 无模态细分数据")
            return
        mod_map = defaultdict(int)
        for d in details_list:
            m_name = getattr(d.modality, 'name', str(d.modality)).split('.')[-1]
            mod_map[m_name] += (d.token_count or 0)
        for m, cnt in mod_map.items():
            print(f"    * 模态 [{m.upper()}] : {cnt} tokens")

    print_modality_details("Prompt / 输入层", getattr(usage, 'prompt_tokens_details', []))
    print("")
    print_modality_details("Candidate / 输出层", getattr(usage, 'candidates_tokens_details', []))
    
    cache_details = getattr(usage, 'cache_tokens_details', [])
    if cache_cnt or cache_details:
        print("")
        print_modality_details("Cached Content / 缓存层", cache_details)

else:
    print("【Token 消耗】: 无 usage_metadata 数据")
print("-" * 50)
