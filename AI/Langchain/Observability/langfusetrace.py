import os
import uuid
from dotenv import load_dotenv
from openai import OpenAI
from langfuse import Langfuse

# Load env variables
load_dotenv()

# Initialize clients
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -----------------------------
# LLM Evaluation Function
# -----------------------------
def evaluate_story_with_llm(story: str) -> float:
    prompt = f"""
    Rate this story from 0 to 1 based on:
    - clarity
    - creativity
    - engagement

    Story:
    {story}

    Return only a number.
    """

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    try:
        return float(response.choices[0].message.content.strip())
    except:
        return 0.5  # fallback


# -----------------------------
# Main Story Generator
# -----------------------------
def generate_story(prompt: str, user_id: str, session_id: str):

    # Create trace
    trace = langfuse.trace(
        name="dynamic-story-generator",
        user_id=user_id,
        session_id=session_id,
        metadata={
            "feature": "story_generation",
            "env": os.getenv("ENV", "dev")
        }
    )

    # Create generation span
    generation = trace.generation(
        name="openai-call",
        model="gpt-4o-mini",
        input=prompt
    )

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a calm, emotional storyteller."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        story = response.choices[0].message.content

        # End generation span
        generation.end(
            output=story,
            usage=response.usage.model_dump() if response.usage else None
        )

        # -----------------------------
        # LLM-based scoring
        # -----------------------------
        llm_score = evaluate_story_with_llm(story)

        langfuse.score(
            trace_id=trace.id,
            observation_id=generation.id,
            name="llm_quality_score",
            value=llm_score,
            comment="Auto-evaluated by LLM"
        )

        # -----------------------------
        # Heuristic scoring example
        # -----------------------------
        length_score = min(len(story) / 500, 1.0)

        langfuse.score(
            trace_id=trace.id,
            observation_id=generation.id,
            name="length_score",
            value=length_score,
            comment="Based on story length"
        )

        # -----------------------------
        # Final aggregated score
        # -----------------------------
        final_score = round((llm_score + length_score) / 2, 2)

        langfuse.score(
            trace_id=trace.id,
            name="final_score",
            value=final_score,
            comment="Combined score"
        )

        return {
            "story": story,
            "scores": {
                "llm": llm_score,
                "length": length_score,
                "final": final_score
            }
        }

    except Exception as e:
        # Log error in generation span
        generation.end(
            output=str(e),
            level="ERROR"
        )
        raise

    finally:
        # Ensure logs are sent
        langfuse.flush()


# -----------------------------
# Main Runner
# -----------------------------
if __name__ == "__main__":
    try:
        user_prompt = input("Enter your story topic: ").strip()

        if not user_prompt:
            raise ValueError("Prompt cannot be empty")

        result = generate_story(
            prompt=user_prompt,
            user_id="kumar",
            session_id=str(uuid.uuid4())
        )

        print("\nGenerated Story:\n")
        print(result["story"])

        print("\nScores:\n")
        print(result["scores"])

    except Exception as e:
        print(f"Error: {e}")