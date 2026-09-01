import os
from dotenv import load_dotenv
from openai import OpenAI
from langfuse import observe, Langfuse
#from langfuse.openai import openai
# from langfuse.decorators import observe


# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key from .env
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Langfuse client with credentials from .env
langfuse_client = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

# Observe OpenAI calls with Langfuse
@observe() # Use the decorator on the function that calls OpenAI
def create_story(client):
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Tell me a short story about a brave knight."}],
        temperature=0.7
    )

# Example usage
try:
    chat_completion = create_story(openai_client)
    print(chat_completion.choices[0].message.content)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    langfuse_client.flush()

