# chat.py

import torch
import config
from model import TinySQLTransformer

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Load model
print("Loading model... please wait")
checkpoint = torch.load(config.checkpoint_path, map_location=device)

vocab_size = checkpoint['vocab_size']
stoi = checkpoint['stoi']
itos = checkpoint['itos']

encode = lambda s: [stoi[c] for c in s if c in stoi]
decode = lambda l: ''.join([itos[i] for i in l])

model = TinySQLTransformer(vocab_size=vocab_size).to(device)
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

print("Model loaded successfully!")
print("=" * 60)
print("SQL Chatbot ready!")
print("Type your question (or 'quit' to exit)")
print("Tip: You can also paste a full Schema + Question")
print("=" * 60)

def generate_response(prompt, max_new_tokens=250):
    # Encode prompt
    context = torch.tensor([encode(prompt)], dtype=torch.long, device=device)
    
    with torch.no_grad():
        generated = model.generate(context, max_new_tokens=max_new_tokens)[0].tolist()
    
    full_text = decode(generated)
    
    # Return only the newly generated part
    return full_text[len(prompt):]

# ==================== CHAT LOOP ====================
while True:
    user_input = input("\nYou: ").strip()
    
    if user_input.lower() in ['quit', 'exit', 'q']:
        print("Goodbye!")
        break
    
    if not user_input:
        continue

    # Automatically format the prompt so the model understands better
    if "### Schema:" in user_input or "CREATE TABLE" in user_input:
        # User already gave a full prompt
        prompt = user_input
    else:
        # User only asked a question → wrap it nicely
        prompt = f"""### Question:
{user_input}

### SQL:
"""

    print("\nBot is thinking...")
    response = generate_response(prompt, max_new_tokens=200)
    
    print("\nBot:")
    print(response.strip())
    print("-" * 50)