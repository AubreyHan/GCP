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

print("-" * 50)
print(f"【Model】: gemini-3.5-flash @ us (Multi-Region)")
print(f"【Prompt】: hello")
print(f"【Response】:\n{response.text}")
print("-" * 50)
