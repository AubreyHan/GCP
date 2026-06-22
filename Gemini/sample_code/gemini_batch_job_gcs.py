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
  src='gs://cloud-samples-data/batch/prompt_for_batch_gemini_predict.jsonl',
  config=CreateBatchJobConfig(dest='gs://hy-ai-bucket')
)

