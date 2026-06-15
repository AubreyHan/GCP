export GOOGLE_APPLICATION_CREDENTIALS="/Users/aubreyhan/Tools/git_repo/GCP/Gemini/sa_key/001.json"

curl -X POST \
  -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d @request.json \
  "https://aiplatform.googleapis.com/v1/projects/hy-ai-demo/locations/global/publishers/google/models/gemini-3.5-flash:generateContent"