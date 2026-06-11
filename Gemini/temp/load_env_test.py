from pickle import TRUE

from dotenv import load_dotenv
import os


while TRUE:
    load_dotenv(override=True)
    print(os.environ.get("PROJECT_ID"))
