import tiktoken

def count_token(text: str, model_name:str="gpt-4o") -> int:
    limit = 100
    encoding = tiktoken.encoding_for_model(model_name)
    return len(encoding.encode(text))

User_input = input("Enter you input:")

User_output = count_token(User_input)

print(User_output)