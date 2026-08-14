# generate.py

import torch
import config
from model import TinySQLTransformer

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Load checkpoint
checkpoint = torch.load(config.checkpoint_path, map_location=device)
vocab_size = checkpoint['vocab_size']
stoi = checkpoint['stoi']
itos = checkpoint['itos']

decode = lambda l: ''.join([itos[i] for i in l])

model = TinySQLTransformer(vocab_size=vocab_size).to(device)
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

print("Model loaded. Generating text...\n")

# Start with empty context
context = torch.zeros((1, 1), dtype=torch.long, device=device)
generated = model.generate(context, max_new_tokens=500)[0].tolist()

print(decode(generated))
