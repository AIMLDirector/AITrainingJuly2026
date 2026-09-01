
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()

# response = client.responses.create(
#     model="gpt-4.1-mini",
#     input="Write a one-sentence bedtime story about a unicorn.",
# )

# print(response.output_text)
while True:
    user_input = input("Enter your prompt (or 'exit' or 'quit' to quit): ")
    if user_input.lower() == 'exit' or user_input.lower() == 'quit':
        break
    
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ],
    )

    print(response.choices[0].message.content)