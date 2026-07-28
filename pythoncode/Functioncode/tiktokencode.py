import tiktoken

# 1. Load the encoding for your model (e.g., GPT-4o, GPT-3.5 Turbo)
encoding = tiktoken.encoding_for_model("gpt-4o")

# 2. Encode text into token IDs
text = "Hello, tiktoken is great!"
tokens = encoding.encode(text)

# 3. Count the tokens
token_count = len(tokens)
print(f"Token count: {token_count}")

# 4. Decode the tokens back into text
original_text = encoding.decode(tokens)
