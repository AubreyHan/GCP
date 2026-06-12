from dotenv import load_dotenv
import os

if load_dotenv(override=True):
    pass

print(os.environ.get("PROJECT_ID"))
