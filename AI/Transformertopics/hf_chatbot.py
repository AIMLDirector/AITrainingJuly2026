# hf_chatbot.py

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

# Choose a model (small & good for chat)
#model_name = "microsoft/Phi-3-mini-4k-instruct"   # Excellent small chat model
# Other good options:
model_name = "Qwen/Qwen2.5-1.5B-Instruct"
# model_name = "HuggingFaceH4/zephyr-7b-beta"     # bigger & stronger

print("Loading model... (first time will download)")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto",
    trust_remote_code=True
)

# Create chat pipeline
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
)

print("\nChatbot is ready! Type 'quit' to exit.\n")

# System prompt specialized for Data Engineering / SQL
system_message = """You are a helpful Data Engineering assistant.
You specialize in SQL, data pipelines, ETL, and database questions.
Answer clearly and give correct SQL when asked."""

messages = [
    {"role": "system", "content": system_message}
]

while True:
    user_input = input("You: ").strip()
    
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    
    if not user_input:
        continue

    # Add user message
    messages.append({"role": "user", "content": user_input})

    # Generate reply
    prompt = tokenizer.apply_chat_template(
        messages, 
        tokenize=False, 
        add_generation_prompt=True
    )

    outputs = pipe(
        prompt,
        max_new_tokens=400,
        do_sample=True,
        temperature=0.3,      # lower = more focused answers
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id
    )

    # Extract only the new response
    full_text = outputs[0]["generated_text"]
    response = full_text[len(prompt):].strip()

    print(f"\nBot: {response}\n")
    print("-" * 60)

    # Add bot reply to conversation history
    messages.append({"role": "assistant", "content": response})