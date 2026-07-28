from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

def genai_func1(user_prompt:str, system_prompt:str ="you are AI asistant for Cloud engineer"):
    client = OpenAI()
    response = client.chat.completions.create(
        model = "gpt-4o",
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": user_prompt}],
        temperature=0.8
        )
    
    
    return response.choices[0].message.content

user_input = input("Enter user prompt input: ")
system_input = input("Enter your system prompt input: ")

output_response = genai_func1(user_input, system_input)

print(output_response)