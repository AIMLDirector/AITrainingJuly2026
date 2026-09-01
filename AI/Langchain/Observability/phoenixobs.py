from phoenix.otel import register
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
load_dotenv()

tracer_provider = register(
  project_name="testproject",
  auto_instrument=True
)


prompt = ChatPromptTemplate.from_template("Explain {topic} in simple terms.")
chain = prompt | ChatOpenAI(model="gpt-4o-mini")
response = chain.invoke({"topic": "the theory of relativity"})