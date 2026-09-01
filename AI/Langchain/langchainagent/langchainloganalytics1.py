import re
from enum import Enum
from typing import Optional 
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()

class SeverityLevel(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class LogAnalysis(BaseModel):
    timestamp: Optional[str] = Field(None, description="The ISO timestamp or date-time when the error occurred")
    severity: SeverityLevel = Field(..., description="The severity level of the logged event")
    service_name: str = Field(description="The microservice, module, or component that threw the error")
    error_message: str = Field(description="The core error message or exception summary")
    stack_trace_snippet: Optional[str] = Field(None, description="The relevant lines from the stack trace")
    root_cause_hypothesis: str = Field(description="A brief hypothesis of why this happened")
    recommended_fix: str = Field(description="Actionable steps to resolve this error")

# Initialize the structured agent
agent = create_agent(
    model="gpt-4.1-mini",
    response_format=LogAnalysis
)

def process_log(log_text: str):
    """Validates the log severity and conditionally routes it to the AI agent."""
    # Convert to uppercase to handle case-insensitive matches safely
    log_upper = log_text.upper()
    
    # 1. Check for WARNING conditions
    if "WARN" in log_upper:
        print(f"⚠️ [Skip] This is a system warning. Skipping AI analysis.")
        return None

    # 2. Check for ERROR or CRITICAL conditions
    elif "ERROR" in log_upper or "CRITICAL" in log_upper or "FATAL" in log_upper:
        print("🚨 [Process] Critical issue detected. Invoking AI analysis agent...")
        
        result = agent.invoke({
            "messages": [
                {
                    "role": "user", 
                    "content": f"Analyze the following application log and provide structured debugging insights:\n\n{log_text}"
                }
            ]
        })
        return result["structured_response"]
        
    # 3. Fallback for unclassified logs
    else:
        print("ℹ️ [Skip] No error pattern identified in the log.")
        return None

# ==========================================
# TEST SCENARIOS
# ==========================================

# Test 1: Warning Log (Will be skipped)
warning_log = "2026-08-31 06:42:10 [auth-service] WARN c.x.a.Filter - JWT Token close to expiration for user_id=4823"
print("\n--- Testing Warning Log ---")
process_log(warning_log)


# Test 2: Error Log (Will be processed by LLM)
error_log = """
2026-08-31 06:42:15 [payment-service] ERROR c.x.p.Engine - Failed to process transaction
java.lang.NullPointerException: return value of getCurrency() is null
    at com.xyz.payment.Engine.validateCurrency(Engine.java:142)
"""
print("\n--- Testing Error Log ---")
analysis = process_log(error_log)

if analysis:
    print("\n=== AI Analysis Report ===")
    print(f"Timestamp:    {analysis.timestamp}")    
    print(f"Severity:     {analysis.severity.value}")
    print(f"Service:      {analysis.service_name}")
    print(f"Error:        {analysis.error_message}")
    print(f"Fix Strategy: {analysis.recommended_fix}")
