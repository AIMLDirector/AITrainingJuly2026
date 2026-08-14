# push_to_hub.py

import torch
from huggingface_hub import login
import config
from model import TinySQLTransformer

# 1. Login (you will be asked for your Hugging Face write token)
login()

# 2. Load the trained model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
checkpoint = torch.load(config.checkpoint_path, map_location=device)

model = TinySQLTransformer(vocab_size=checkpoint['vocab_size'])
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# 3. Push to Hub
repo_id = "premkumar/tiny-sql-transformer-data-eng"   # ← CHANGE THIS

model.push_to_hub(
    repo_id,
    commit_message="Tiny Transformer trained from scratch on gretelai/synthetic_text_to_sql (Data Engineering)"
)

print(f"\nModel successfully uploaded → https://huggingface.co/{repo_id}")