# inspect_data.py

from datasets import load_dataset
import config

print("Loading dataset...")
dataset = load_dataset(config.dataset_name, split="train")
dataset = dataset.shuffle(seed=42).select(range(config.num_examples))

print(f"\nTotal examples used for training: {len(dataset)}")
print("=" * 70)

# Show first 3 examples
for i in range(20):
    row = dataset[i]
    print(f"\n----- Example {i+1} -----")
    print(f"Domain       : {row['domain']}")
    print(f"Complexity   : {row['sql_complexity']}")
    print(f"Task Type    : {row['sql_task_type']}")
    print(f"\nQuestion:\n{row['sql_prompt']}")
    print(f"\nSchema:\n{row['sql_context'][:300]}...")
    print(f"\nSQL:\n{row['sql']}")
    print(f"\nExplanation:\n{row['sql_explanation'][:200]}...")
    print("=" * 70)