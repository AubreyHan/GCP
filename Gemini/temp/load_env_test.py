from dotenv import load_dotenv
import os

load_dotenv(override=True)
print(os.environ.get("PROJECT_ID"))
print(os.getenv("PROJECT_ID"))