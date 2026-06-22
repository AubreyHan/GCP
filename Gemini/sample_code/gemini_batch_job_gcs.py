import time
from google import genai
from google.genai.types import CreateBatchJobConfig, JobState, HttpOptions

from Gemini.loopit.loopit import project_id

client = genai.Client(
  enterprise=True,
  project='cloud-llm-preview4',
  location='global'
)

job = client.batches.create(
  model='gemini-2.5-flash',
  src='gs://cloud-samples-data/batch/prompt_for_batch_gemini_predict.jsonl',
  config=CreateBatchJobConfig(dest='gs://hy-ai-bucket')
)

print(f"Job name: {job.name}")
print(f"Job state: {job.state}")

completed_states = {
    JobState.JOB_STATE_SUCCEEDED,
    JobState.JOB_STATE_FAILED,
    JobState.JOB_STATE_CANCELLED,
    JobState.JOB_STATE_PAUSED,
}

while job.state not in completed_states:
    time.sleep(30)
    job = client.batches.get(name=job.name)
    print(f"Job state: {job.state}")