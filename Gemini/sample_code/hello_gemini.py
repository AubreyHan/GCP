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
    print(f"【Token 消耗细化统计】")
    print(f"  - Prompt Tokens (输入)      : {getattr(usage, 'prompt_token_count', 0)}")
    print(f"  - Candidate Tokens (输出)   : {getattr(usage, 'candidates_token_count', 0)}")
    print(f"  - Total Tokens (总计)       : {getattr(usage, 'total_token_count', 0)}")
    
    cached = getattr(usage, 'cached_content_token_count', 0)
    thoughts = getattr(usage, 'thoughts_token_count', 0)
    if cached:
        print(f"  * Cached Content Tokens    : {cached}")
    if thoughts:
        print(f"  * Thoughts Tokens (思考推理): {thoughts}")
else:
    print("【Token 消耗】: 无 usage_metadata 数据")
print("-" * 50)
