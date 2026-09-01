from dotenv import load_dotenv
import os
load_dotenv()
openapikey = os.getenv("OPENAI_API_KEY")
print(openapikey)

