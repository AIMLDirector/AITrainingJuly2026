from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
 # initialize the model with the desired parameters
client = ChatOpenAI(model="gpt-4o-mini")

# messages
messages = [
    ("system","You are a helpful assistant that translates English to French. Translate the user sentence.",),
    ("human", "I love programming."),
]
# executionmessages
response = client.invoke(messages)
print(response.text)

