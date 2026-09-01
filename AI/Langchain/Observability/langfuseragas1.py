import os
import uuid
from dotenv import load_dotenv
from openai import OpenAI
from langfuse import observe, Langfuse

# RAGAS 0.4.3
from ragas import evaluate
from ragas.metrics import Faithfulness, AnswerRelevancy
from datasets import Dataset

# LangChain OpenAI (REQUIRED for RAGAS 0.4.x)
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


# ---------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------
load_dotenv()

# ---------------------------------------------------
# Langfuse Setup
# ---------------------------------------------------
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

# ---------------------------------------------------
# OpenAI Client (For Generation)
# ---------------------------------------------------
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------------------------------
# Evaluation LLM (Used ONLY for RAGAS)
# Keep temperature=0 for deterministic scoring
# ---------------------------------------------------
eval_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=2048
)

# ---------------------------------------------------
# Embeddings (Required for AnswerRelevancy)
# ---------------------------------------------------
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)


# ---------------------------------------------------
# LLM Generation Function
# ---------------------------------------------------
@observe(name="dynamic-story-generator")
def generate_story(prompt: str, user_id: str, session_id: str):

    langfuse.update_current_span(
        user_id=user_id,
        session_id=session_id,
        tags=["demo", "ragas", "openai"],
        metadata={
            "feature": "story_generation",
            "environment": "dev"
        }
    )

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a creative storyteller."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=800  # prevent massive outputs
    )

    return response


# ---------------------------------------------------
# RAGAS Evaluation (0.4.3 Correct Pattern)
# ---------------------------------------------------
def evaluate_with_ragas(question: str, answer: str):

    data = {
        "question": [question],
        "answer": [answer],
        "contexts": [["Creative storytelling task without retrieval context."]]
    }

    dataset = Dataset.from_dict(data)

    # IMPORTANT: Inject LLM & embeddings into metric objects
    metrics = [
        Faithfulness(llm=eval_llm),
        AnswerRelevancy(llm=eval_llm, embeddings=embeddings)
    ]

    result = evaluate(
        dataset,
        metrics=metrics
    )

    return result


# ---------------------------------------------------
# Main Execution
# ---------------------------------------------------
if __name__ == "__main__":

    try:
        user_prompt = input("Enter your story topic: ")
        user_id = "kumar"
        session_id = str(uuid.uuid4())

        print("\nGenerating story...\n")

        result = generate_story(user_prompt, user_id, session_id)
        story = result.choices[0].message.content

        print("Generated Story:\n")
        print(story)

        # -------------------------
        # Run RAGAS Evaluation
        # -------------------------
        print("\nRunning RAGAS evaluation...\n")

        ragas_result = evaluate_with_ragas(user_prompt, story)

        scores = ragas_result.to_dict()

        faith_score = float(scores["faithfulness"][0])
        relevancy_score = float(scores["answer_relevancy"][0])

        print("RAGAS Scores:")
        print(f"Faithfulness: {faith_score}")
        print(f"Answer Relevancy: {relevancy_score}")

        # -------------------------
        # Log Scores to Langfuse
        # (New API — score() removed)
        # -------------------------
        langfuse.create_score(
            name="faithfulness",
            value=faith_score
        )

        langfuse.create_score(
            name="answer_relevancy",
            value=relevancy_score
        )

        print("\nScores logged to Langfuse successfully.")

    except Exception as e:
        print("Error:", e)

    finally:
        langfuse.flush()