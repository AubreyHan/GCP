from google import genai

# 按照最新的 multi-region 方式，使用 "us" 作为区域标识
client = genai.Client(
    project="cloud-llm-preview4",
    location="us",
    vertexai=True,
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
