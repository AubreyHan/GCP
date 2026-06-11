from pickle import TRUE

from dotenv import load_dotenv
import os

load_dotenv(override=True)

if TRUE:
    print(os.environ.get("PROJECT_ID"))
