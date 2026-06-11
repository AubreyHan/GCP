from pickle import TRUE

from dotenv import load_dotenv
import os


while TRUE:
    load_dotenv()
    print(os.environ.get("PROJECT_ID"))
