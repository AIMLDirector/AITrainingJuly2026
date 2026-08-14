from ollama import chat


while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    response = chat(
        model="qwenmodel_Development:latest",
        messages=[
            {"role": "user", "content": user_input}
        ]
    )

    print("AI:", response["message"]["content"])