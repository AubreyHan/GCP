from dotenv import load_dotenv

if load_dotenv(override=True):
    pass

print(os.environ.get("PROJECT_ID"))
