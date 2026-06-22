import time
from google import genai
from google.genai.types import CreateBatchJobConfig, JobState, HttpOptions

from Gemini.loopit.loopit import project_id

client = genai.client(

)