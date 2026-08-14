# sql_chatbot.py

from transformers import pipeline
import torch

# Good SQL-focused models
model_name = "defog/sqlcoder-7b-2"          # Strong for SQL
# or smaller: "NumbersStation/nsql-llama-2-7B"

pipe = pipeline(
    "text-generation",
    model=model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)

print("SQL Chatbot ready! Ask any question about data.\n")

while True:
    question = input("You: ").strip()
    if question.lower() in ["quit", "exit"]:
        break

    prompt = f"""### Instruction:
Generate a correct SQL query for the following question.

### Question:
{question}

### SQL:
"""

    result = pipe(
        prompt,
        max_new_tokens=200,
        temperature=0.1,
        do_sample=False
    )[0]["generated_text"]

    # Extract SQL part
    sql = result.split("### SQL:")[-1].strip()
    print(f"\nBot (SQL):\n{sql}\n")
    print("-" * 50)