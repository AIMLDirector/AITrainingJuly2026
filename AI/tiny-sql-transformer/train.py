# train.py

import torch
import config
from model import TinySQLTransformer
from data import prepare_data

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# Prepare data
train_data, val_data, vocab_size, encode, decode, stoi, itos = prepare_data()

# Create model
model = TinySQLTransformer(vocab_size=vocab_size).to(device)
print(f"Model parameters: {sum(p.numel() for p in model.parameters())/1e6:.2f}M")

optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)

def get_batch(split):
    data = train_data if split == 'train' else val_data
    ix = torch.randint(len(data) - config.block_size, (config.batch_size,))
    x = torch.stack([data[i:i+config.block_size] for i in ix])
    y = torch.stack([data[i+1:i+config.block_size+1] for i in ix])
    return x.to(device), y.to(device)

@torch.no_grad()
def estimate_loss():
    model.eval()
    out = {}
    for split in ['train', 'val']:
        losses = torch.zeros(config.eval_iters)
        for k in range(config.eval_iters):
            X, Y = get_batch(split)
            _, loss = model(X, Y)
            losses[k] = loss.item()
        out[split] = losses.mean()
    model.train()
    return out

# Training loop
print("Starting training...")
for iter in range(config.max_iters):
    if iter % config.eval_interval == 0 or iter == config.max_iters - 1:
        losses = estimate_loss()
        print(f"step {iter:4d} | train loss {losses['train']:.4f} | val loss {losses['val']:.4f}")

    xb, yb = get_batch('train')
    logits, loss = model(xb, yb)
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    optimizer.step()

# Save checkpoint
torch.save({
    'model_state_dict': model.state_dict(),
    'vocab_size': vocab_size,
    'stoi': stoi,
    'itos': itos,
    'config': {
        'n_embd': config.n_embd,
        'n_head': config.n_head,
        'n_layer': config.n_layer,
        'block_size': config.block_size,
        'dropout': config.dropout,
    }
}, config.checkpoint_path)

print(f"\nTraining finished! Checkpoint saved to {config.checkpoint_path}")