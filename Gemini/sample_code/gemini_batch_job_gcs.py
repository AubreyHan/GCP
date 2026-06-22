import time
from google import genai
from google.genai.types import CreateBatchJobConfig, JobState, HttpOptions

client = genai.client(
  vertex
)