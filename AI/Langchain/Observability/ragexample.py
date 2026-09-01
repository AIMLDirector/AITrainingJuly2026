import os
import asyncio
from openai import AsyncOpenAI
from ragas_examples.improve_rag.rag import RAG, BM25Retriever
from dotenv import load_dotenv
load_dotenv()
# Set up OpenAI client
# os.environ["OPENAI_API_KEY"] = "<your_key>"
openai_client = AsyncOpenAI()

# Create retriever and RAG system
retriever = BM25Retriever()
rag = RAG(openai_client, retriever)

# Query the system
question = "What architecture is the `tokenizers-linux-x64-musl` binary designed for?"
result = asyncio.run(rag.query(question))
print(f"Answer: {result['answer']}")