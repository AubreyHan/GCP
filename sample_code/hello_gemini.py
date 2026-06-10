from google import genai

# 根据您的显式要求，此处将 location 从项目规范的 "global" 破例设为了 US 区域 "us-central1"
client = genai.Client(
    project="cloud-llm-preview4",
    location="us-central1",
    vertexai=True,
)

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="hello",
)

print("-" * 50)
print(f"【Model】: gemini-3.5-flash @ us-central1")
print(f"【Prompt】: hello")
print(f"【Response】:\n{response.text}")
print("-" * 50)
