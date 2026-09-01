import os
from dotenv import load_dotenv
from openai import OpenAI
from langfuse import observe, Langfuse

from ragas import evaluate
from ragas.metrics.collections import AnswerRelevancy
from ragas.llms import llm_factory
from ragas.embeddings import embedding_factory
from datasets import Dataset

load_dotenv()
langfuse = Langfuse()
openai_client = OpenAI()

instructor_llm = llm_factory("gpt-4o-mini", client=openai_client)
ragas_embeddings = embedding_factory("openai", "text-embedding-3-small", client=openai_client)

# Set user_id/session_id directly in decorator
@observe(name="kafka-story-eval", user_id="kumar", session_id="sess_abc123")
def generate_and_evaluate(topic: str):

    # Only span-level updates here
    langfuse.update_current_span(
        metadata={"tags": ["ragas", "story"]},
        input={"topic": topic}
    )

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a creative storyteller."},
            {"role": "user", "content": f"Explain {topic} as a story"}
        ],
        temperature=0.8,
        max_tokens=400
    )
    story = response.choices[0].message.content
    langfuse.update_current_span(output={"story": story})

    # RAGAS eval
    dataset = Dataset.from_dict({
        "question": [topic],
        "answer": [story],
        "contexts": [["Kafka uses ZooKeeper, brokers, topics, and consumer groups."]]
    })

    result = evaluate(
        dataset,
        metrics=[AnswerRelevancy(llm=instructor_llm, embeddings=ragas_embeddings)]
    )
    score = float(result["answer_relevancy"][0])

    # This works in 4.5.1 - you saw it in help()
    langfuse.score_current_trace(
        name="answer_relevancy",
        value=score,
        comment="Ragas 0.4.3"
    )

    return story, score

if __name__ == "__main__":
    try:
        story, rel_score = generate_and_evaluate("how to setup kafka")
        print("Story:\n", story)
        print(f"\nAnswer Relevancy: {rel_score:.4f}")
    finally:
        langfuse.flush()