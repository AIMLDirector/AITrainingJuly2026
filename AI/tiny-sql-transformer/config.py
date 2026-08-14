# config.py

# Model architecture
batch_size = 32
block_size = 128          # context length
n_embd = 128
n_head = 4
n_layer = 4
dropout = 0.1

# Training
learning_rate = 3e-4
max_iters = 3000
eval_interval = 300
eval_iters = 30

# Data
num_examples = 8000       # how many samples to take from the dataset
dataset_name = "gretelai/synthetic_text_to_sql"

# Paths
checkpoint_path = "checkpoint.pt"