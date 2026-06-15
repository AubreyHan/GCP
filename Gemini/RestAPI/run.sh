# ==================== 1. 基础参数配置 ====================
# 你的 GCP 项目 ID
export PROJECT_ID="hy-ai-demo"

# 你想要假冒的目标服务账号
export TARGET_SA="demo001-20260615-001del@hy-ai-demo.iam.gserviceaccount.com"

# ==================== 2. 核心：动态模拟换票 ====================
# 这一步会绕过本地 ADC 缓存，直接调用 IAM 接口，用你当前的个人登录凭据现场换取服务账号的 Access Token
echo "正在尝试模拟服务账号并生成临时 Token..."
export IMPERSONATED_TOKEN=$(gcloud auth application-default print-access-token --impersonate-service-account=demo001-20260615-001del@hy-ai-demo.iam.gserviceaccount.com)

# 简单验证 Token 是否成功拿到
if [ -z "$IMPERSONATED_TOKEN" ]; then
    echo "❌ 错误：未能成功生成模拟 Token，请检查云端 IAM Token Creator 权限是否同步完成。"
    return 1
else
    echo " 成功：已拿到合法的服务账号模拟 Token！"
fi

# ==================== 3. 发起 Gemini 请求 ====================
# 使用拿到的临时 Token，通过 curl 强刷 Vertex AI Gemini 3.5 Flash 接口
echo "正在发起 Gemini API 请求..."
curl -X POST \
  -H "Authorization: Bearer ${IMPERSONATED_TOKEN}" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{
    "contents": {
        "role": "user",
        "parts": [
            {
                "text": "请用一句话简述什么是谷歌云的应用默认凭据（ADC）？"
            }
        ]
    },
    "generationConfig": {
        "temperature": 0.2,
        "maxOutputTokens": 1024
    }
}' \
  "https://aiplatform.googleapis.com/v1/projects/hy-ai-demo/locations/global/publishers/google/models/gemini-3.5-flash:generateContent"