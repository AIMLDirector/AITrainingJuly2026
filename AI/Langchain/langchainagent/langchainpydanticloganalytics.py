from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from dotenv import load_dotenv

# Load environment variables (API keys)
load_dotenv()

class SeverityLevel(str, Enum):
    """The classification of the error impact."""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class LogAnalysis(BaseModel):
    """Structured analysis framework for an application error log."""
    timestamp: Optional[str] = Field(None, description="The ISO timestamp or date-time when the error occurred")
    severity: SeverityLevel = Field(..., description="The severity level of the logged event")
    service_name: str = Field(description="The microservice, module, or component that threw the error")
    error_message: str = Field(description="The core error message or exception summary")
    stack_trace_snippet: Optional[str] = Field(None, description="The most relevant lines from the stack trace identifying the root failure line")
    root_cause_hypothesis: str = Field(description="A brief hypothesis of why this error happened based on the log context")
    recommended_fix: str = Field(description="Actionable steps or debugging paths to resolve or mitigate this error")

# Initialize the structured agent
agent = create_agent(
    model="gpt-4.1-mini",
    response_format=LogAnalysis
)

# Sample messy application error log
sample_log = """
2026-08-31 06:42:15,312 [payment-processing-service] ERROR c.x.p.Engine - Failed to process transaction checkout_94823a
java.lang.NullPointerException: Cannot invoke "String.equals(Object)" because the return value of "com.xyz.payment.UserSession.getCurrency()" is null
    at com.xyz.payment.Engine.validateCurrency(Engine.java:142)
    at com.xyz.payment.Engine.process(Engine.java:58)
    at com.xyz.payment.Controller.handleCheckout(Controller.java:22)
    at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:379)
"""

# Invoke the agent to extract and analyze the data
result = agent.invoke({
    "messages": [
        {
            "role": "user", 
            "content": f"Analyze the following application log and provide structured debugging insights:\n\n{sample_log}"
        }
    ]
})

# Access the Pydantic instance directly from structured_response
analysis: LogAnalysis = result["structured_response"]

# Display the structured output
print("=== Log Analysis Report ===")
print(f"Timestamp:    {analysis.timestamp}")
print(f"Severity:     {analysis.severity.value}")
print(f"Service:      {analysis.service_name}")
print(f"Error:        {analysis.error_message}")
print(f"Snippet:      {analysis.stack_trace_snippet}")
print(f"Hypothesis:   {analysis.root_cause_hypothesis}")
print(f"Fix Strategy: {analysis.recommended_fix}")
