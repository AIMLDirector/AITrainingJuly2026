import os
import uuid
from dotenv import load_dotenv
from openai import OpenAI
from langfuse import observe, Langfuse

# RAGAS imports
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from datasets import Dataset

load_dotenv()

# -------------------------
# Langfuse Setup
# -------------------------
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------
# LLM Function
# -------------------------
@observe(name="dynamic-story-generator")
def generate_story(prompt: str, user_id: str, session_id: str):

    langfuse.update_current_trace(
        user_id=user_id,
        session_id=session_id,
        tags=["demo", "llm", "openai"],
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
        temperature=0.8
    )

    return response


# -------------------------
# RAGAS Evaluation Function
# -------------------------
def evaluate_with_ragas(question, answer):

    data = {
        "question": [question],
        "answer": [answer],
        "contexts": [["Creative storytelling task without retrieval context"]]
    }

    dataset = Dataset.from_dict(data)

    result = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy]
    )

    return result


# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    try:
        user_prompt = input("Enter your story topic: ")
        user_id = "kumar"
        session_id = str(uuid.uuid4())

        result = generate_story(user_prompt, user_id, session_id)

        story = result.choices[0].message.content

        print("\nGenerated Story:\n")
        print(story)

        # -------------------------
        # Run RAGAS Evaluation
        # -------------------------
        print("\nRunning RAGAS evaluation...\n")

        ragas_result = evaluate_with_ragas(user_prompt, story)

        print(ragas_result)

        # -------------------------
        # Log RAGAS metrics to Langfuse
        # -------------------------
        langfuse.score(
            name="faithfulness",
            value=float(ragas_result["faithfulness"][0])
        )

        langfuse.score(
            name="answer_relevancy",
            value=float(ragas_result["answer_relevancy"][0])
        )

    except Exception as e:
        print(f"Error: {e}")

    finally:
        langfuse.flush()