
import os
import openai
from dotenv import load_dotenv
from promptflow.tracing import start_trace


# Correct instrumentation for OpenAI
from opentelemetry import trace
from opentelemetry.instrumentation.openai import OpenAIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

# Start Promptflow tracing and configure OpenTelemetry
start_trace()
OpenAIInstrumentor().instrument()

# Configure a console span exporter to view logs in the terminal
span_exporter = ConsoleSpanExporter()
tracer_provider = trace.get_tracer_provider()
tracer_provider.add_span_processor(SimpleSpanProcessor(span_exporter))

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

# Initialize the OpenAI client
client = openai.Client(api_key=api_key)

# Make the OpenAI API call
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Hello! How can I use the OpenAI API in Python?"}
        ]
    )
    print(response.choices[0].message.content)
except Exception as e:
    print(f"An error occurred: {e}")
