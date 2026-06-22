import time
from google import genai
from google.genai.types import CreateBatchJobConfig, JobState, HttpOptions

from Gemini.loopit.loopit import project_id

client = genai.Client(
  enterprise=True,
  project='hy-ai-demo',
  location='global'
)

job = client.batches.create(
  model='gemini-2.5-flash',
  src='https://storage.googleapis.com/cloud-samples-data/generative-ai/batch/batch_requests_for_multimodal_input_2.jsonl',
  config=CreateBatchJobConfig()
),