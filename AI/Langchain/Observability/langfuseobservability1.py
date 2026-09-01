
import os
import uuid

from dotenv import load_dotenv
from openai import OpenAI
from langfuse import Langfuse

load_dotenv()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_story(prompt, user_id, session_id):

    with langfuse.start_as_current_observation(
        name="dynamic-story-generator"
    ) as observation:

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a creative storyteller."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.8
        )

        observation.update(
            input=prompt,
            output=response.choices[0].message.content,
            metadata={
                "user_id": user_id,
                "session_id": session_id,
                "feature": "story_generation",
                "environment": "dev"
            }
        )

        return response


if __name__ == "__main__":

    try:

        topic = input("Enter your story topic: ")

        result = generate_story(
            topic,
            user_id="kumar",
            session_id=str(uuid.uuid4())
        )

        print("\nGenerated Story:\n")
        print(result.choices[0].message.content)

    except Exception as e:
        print("Error:", e)

    finally:
        langfuse.flush()

