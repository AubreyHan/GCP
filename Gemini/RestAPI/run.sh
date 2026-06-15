curl -X POST \
  -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d @request.json \
  "https://aiplatform.googleapis.com/v1/projects/hy-ai-demo/locations/us-central1/publishers/google/models/gemini-2.5-flash-001:generateContent"