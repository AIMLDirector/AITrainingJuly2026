# data.py

import torch
from datasets import load_dataset
import config

def prepare_data():
    print("Loading dataset...")
    dataset = load_dataset(config.dataset_name, split="train")
    dataset = dataset.shuffle(seed=42).select(range(config.num_examples))

    texts = []
    for row in dataset:
        sample = f"""### Schema:
{row['sql_context']}

### Question:
{row['sql_prompt']}

### SQL:
{row['sql']}

### Explanation:
{row['sql_explanation']}

"""
        texts.append(sample)

    full_text = "\n\n".join(texts)
    print(f"Total characters: {len(full_text):,}")

    # Character-level vocabulary
    chars = sorted(list(set(full_text)))
    vocab_size = len(chars)
    stoi = {ch: i for i, ch in enumerate(chars)}
    itos = {i: ch for i, ch in enumerate(chars)}

    encode = lambda s: [stoi[c] for c in s]
    decode = lambda l: ''.join([itos[i] for i in l])

    data = torch.tensor(encode(full_text), dtype=torch.long)
    n = int(0.9 * len(data))
    train_data = data[:n]
    val_data = data[n:]

    print(f"Vocab size: {vocab_size}")
    print(f"Train tokens: {len(train_data):,}")
    print(f"Val tokens:   {len(val_data):,}")

    return train_data, val_data, vocab_size, encode, decode, stoi, itos