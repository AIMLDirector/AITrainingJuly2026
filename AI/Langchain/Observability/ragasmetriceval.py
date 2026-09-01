import os
import asyncio
import pandas as pd
from ragas import Dataset, experiment
from ragas.metrics import DiscreteMetric

# 1. Initialize RAG client (Mock for demonstration)
class MockRAGClient:
    def query(self, question: str) -> dict:
        # Simulate retrieval/generation for demonstration
        if "Ragas 0.3" in question:
            return {"answer": "Ragas 0.3 is an open-source evaluation framework...", "logs": "chunk_1"}
        return {"answer": "Unknown topic", "logs": "no_context"}

rag_client = MockRAGClient()

# 2. Define LLM-based Metric
# Uses a DiscreteMetric to check response vs grading notes
correctness_metric = DiscreteMetric(
    name="correctness",
    prompt="Check if response matches grading notes. Return 'pass' or 'fail'.\nResponse: {response} Notes: {grading_notes}",
    allowed_values=["pass", "fail"],
)

# 3. Create Dataset
# Defines the questions and expected answers
def load_evaluation_dataset():
    data_samples = [
        {"question": "What is Ragas 0.3?", "grading_notes": "- framework - LLM apps"},
        {"question": "How do experiments work?", "grading_notes": "- track results"},
    ]
    return Dataset(name="rag_test_dataset", backend="local/csv", root_dir="evals", data=data_samples)

# 4. Asynchronous Experiment Loop
# The @experiment decorator manages execution and logging
@experiment()
async def run_evaluation_loop(row):
    response = rag_client.query(row["question"])
    score = correctness_metric.score(
        response=response.get("answer", ""),
        grading_notes=row["grading_notes"]
    )
    return {
        **row,
        "response": response.get("answer", ""),
        "score": score.value,
        "log_file": response.get("logs", ""),
    }

# 5. Execute Evaluation
async def main():
    dataset = load_evaluation_dataset()
    results = await run_evaluation_loop.arun(dataset)
    # print(pd.DataFrame(results)[["question", "score", "response"]])
    df = results.to_pandas()
    print(df[["question", "score", "response"]])

if __name__ == "__main__":
    asyncio.run(main())
