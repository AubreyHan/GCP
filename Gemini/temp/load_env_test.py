from dotenv import load_dotenv

load_dotenv(override=True)
print(os.environ.get("MY_PROJECT_ENV"))
