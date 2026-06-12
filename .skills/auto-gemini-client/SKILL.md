---
name: auto-gemini-client
description: >
  CRITICAL: You MUST use this skill whenever you are generating or modifying a Gemini Python program.
  It automatically adds or standardizes the global GenAI Client definition to point to the designated
  project and Vertex AI global endpoint.
---

# Auto Gemini Client Initialization

## Mandatory Rules for Gemini Python Code Generation

Whenever you create a new Python program or modify an existing script that uses the Google GenAI SDK (`google-genai`), you MUST ensure that the client is initialized using the exact configuration below:

```python
from google import genai
from dotenv import load_dotenv
import os

load_dotenv(override=True)
project_id = os.environ.get("PROJECT_ID")

client = genai.Client(
    project="cloud-llm-preview4",
    location="global",
    vertexai=True,
)
```

### Constraints & Anti-Patterns
1. **Never use standard API keys**: Do not use `api_key=...` or rely on `GEMINI_API_KEY` environment variables. Always enable `vertexai=True`.
2. **Exact project ID**: Must match `"cloud-llm-preview4"`. Do not invent placeholder projects.
3. **Global location**: Must set `location="global"`.

By standardizing this definition, all project scripts remain fully authenticated against the correct enterprise preview cluster.
