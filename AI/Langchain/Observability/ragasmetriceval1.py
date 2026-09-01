import os
import asyncio
import pandas as pd
from ragas import EvaluationDataset, experiment
from ragas.metrics import DiscreteMetric

# ==========================================
# 1. Mock RAG Application Pipeline
# ==========================================
class MockRAGClient:
    def query(self, question: str) -> dict:
        """Simulates RAG production engine outputs"""
        if "Ragas 0.4" in question or "Ragas 0.3" in question:
            return {
                "answer": "Ragas uses an experiments-first, metrics-based evaluation framework.", 
                "logs": "chunk_id_104"
            }
        return {"answer": "Information not found in context.", "logs": "no_chunks"}

rag_client = MockRAGClient()

# ==========================================
# 2. Metric Setup
# ==========================================
# Using the DiscreteMetric structure to compute categorical evaluation scores
correctness_metric = DiscreteMetric(
    name="correctness",
    prompt="Check if response contains elements matching the grading notes. Return 'pass' or 'fail'.\nResponse: {response}\nGrading Notes: {grading_notes}",
    allowed_values=["pass", "fail"],
)

# ==========================================
# 3. Dataset Assembly
# ==========================================
def load_evaluation_dataset() -> EvaluationDataset:
    data_samples = [
        {"query": "What is Ragas 0.4?", "grading_notes": "- framework - evaluation - metrics"},
        {"query": "How do Ragas experiments work?", "grading_notes": "- track changes - run metrics"},
    ]
    
    # Initialize local EvaluationDataset structure
    dataset = EvaluationDataset(name="rag_test_dataset", backend="local/csv", root_dir="evals")
    
    # Safely load the dictionary rows into the active dataset memory tracking
    for sample in data_samples:
        dataset.append(sample)
        
    dataset.save()
    return dataset

# ==========================================
# 4. Asynchronous Evaluation Runner
# ==========================================
@experiment()
async def run_experiment(row):
    """
    Ragas wraps this function. It maps dataset fields natively.
    Input 'row' contains keys defined in your dataset ('query', 'grading_notes').
    """
    # Execute application lookup
    response_payload = rag_client.query(row.get("query"))
    generated_text = response_payload.get("answer", "")
    
    # Calculate metric using keyword mapping arguments
    metric_result = correctness_metric.score(
        response=generated_text,
        grading_notes=row.get("grading_notes")
    )
    
    # Return flat dictionary mapping keys explicitly
    return {
        **row,
        "response": generated_text,
        "score": metric_result.value,
        "log_file": response_payload.get("logs", ""),
    }

# ==========================================
# 5. Main Control Block
# ==========================================
async def main():
    print("Preparing tracking dataset...")
    dataset = load_evaluation_dataset()
    
    print("Executing evaluation experiment tracking...")
    # FIX: Call the wrapper directly in asyncio; Ragas natively orchestrates parallel tracking
    results = await run_experiment(dataset)
    
    print("\n--- Available Columns in Results ---")
    # Clean dictionary generation prevents Pandas column index crashes
    df = pd.DataFrame(results)
    print(list(df.columns))
    
    print("\n--- Evaluation Results ---")
    # Safely select present keys to print cleanly
    display_cols = [c for c in ["query", "score", "response", "grading_notes"] if c in df.columns]
    print(df[display_cols])

if __name__ == "__main__":
    # Ensure OPENAI_API_KEY environment variable is set for your DiscreteMetric LLM judge
    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = "mock-key-for-local-runs"
        
    asyncio.run(main())
