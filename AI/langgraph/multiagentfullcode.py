from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
import os

load_dotenv()

class KafkaLogState(TypedDict):
    raw_log: str
    extracted_info: str
    root_cause: str
    solution: str
    ticket_number: str
    ticket_sys_id: str
    ticket_url: str
    updated_ticket: str          # ← added


# ---------------- ServiceNow Config ----------------
SNOW_INSTANCE = "https://dev266578.service-now.com"
SNOW_USER = "admin"
SNOW_PASSWORD = "8QrOah5Ug^C@"

auth = HTTPBasicAuth(SNOW_USER, SNOW_PASSWORD)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
# --------------------------------------------------

llm = ChatOpenAI(model="gpt-4o-mini")


def log_extraction(state: KafkaLogState) -> dict:
    """Filter out noise and extract critical error patterns from Kafka logs."""
    prompt = f"""You are a log analyst. Analyze the following Kafka log and extract critical error patterns, including error messages, timestamps, and any relevant context.

Kafka log:
{state['raw_log']}

Provide a structured summary of the critical error patterns."""

    response = llm.invoke(prompt)
    return {"extracted_info": response.content}


def root_cause_analysis(state: KafkaLogState) -> dict:
    """Analyze the extracted information to identify potential root causes."""
    prompt = f"""You are a root cause analyst. Based on the extracted information from the Kafka log, identify potential root causes for the critical errors.

Extracted information:
{state['extracted_info']}

Provide a detailed analysis of potential root causes."""

    response = llm.invoke(prompt)
    return {"root_cause": response.content}


def incident_ticket_creation(state: KafkaLogState) -> dict:
    """Create a ServiceNow Incident from the analysis."""
    
    short_desc = "Kafka Producer Timeout - Automated Detection"
    description = f"""**Automated Kafka Log Analysis**

**Raw Log:**
{state.get('raw_log', 'N/A')}

**Extracted Critical Info:**
{state.get('extracted_info', 'N/A')}

**Root Cause Analysis:**
{state.get('root_cause', 'N/A')}
"""

    payload = {
        "short_description": short_desc,
        "description": description,
        "urgency": "2",
        "impact": "2",
        "category": "software",
        "subcategory": "middleware",
        "contact_type": "monitoring",
        "caller_id": "admin"
    }

    url = f"{SNOW_INSTANCE}/api/now/table/incident"
    
    try:
        response = requests.post(url, auth=auth, headers=headers, json=payload, timeout=30)
        
        if response.status_code in (200, 201):
            result = response.json()["result"]
            number = result["number"]
            sys_id = result["sys_id"]
            ticket_url = f"{SNOW_INSTANCE}/nav_to.do?uri=incident.do?sys_id={sys_id}"
            
            print(f"✅ Incident created: {number}")
            return {
                "ticket_number": number,
                "ticket_sys_id": sys_id,
                "ticket_url": ticket_url
            }
        else:
            print(f"❌ Failed to create incident: {response.status_code}")
            print(response.text)
            return {
                "ticket_number": "ERROR",
                "ticket_sys_id": "",
                "ticket_url": ""
            }
    except Exception as e:
        print(f"❌ Exception while creating ticket: {e}")
        return {
            "ticket_number": "ERROR",
            "ticket_sys_id": "",
            "ticket_url": ""
        }


def solution_agent(state: KafkaLogState) -> dict:
    """Suggest a solution based on the root cause."""
    prompt = f"""You are a Kafka expert. Based on the root cause analysis below, suggest concrete remediation steps.

Root Cause:
{state['root_cause']}

Provide clear, actionable solutions."""
    
    response = llm.invoke(prompt)
    return {"solution": response.content}


def incident_ticket_update(state: KafkaLogState) -> dict:
    """Update the existing incident with the solution / work notes."""
    
    if not state.get("ticket_sys_id"):
        return {"updated_ticket": "No ticket to update (creation failed or skipped)"}

    work_notes = f"""**AI Suggested Solution:**

{state.get('solution', 'No solution provided')}
"""

    payload = {
        "work_notes": work_notes
        # "state": "2",  # optional: set to In Progress
    }

    url = f"{SNOW_INSTANCE}/api/now/table/incident/{state['ticket_sys_id']}"
    
    try:
        response = requests.patch(url, auth=auth, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ Ticket {state['ticket_number']} updated")
            return {"updated_ticket": f"Updated {state['ticket_number']} with solution"}
        else:
            print(f"❌ Update failed: {response.status_code}")
            print(response.text)
            return {"updated_ticket": "Update failed"}
    except Exception as e:
        print(f"❌ Exception while updating ticket: {e}")
        return {"updated_ticket": "Update failed (exception)"}


# ---------------- Build the graph ----------------
builder = StateGraph(KafkaLogState)

builder.add_node("log_extraction", log_extraction)
builder.add_node("root_cause_analysis", root_cause_analysis)
builder.add_node("incident_ticket_creation", incident_ticket_creation)
builder.add_node("solution_agent", solution_agent)
builder.add_node("incident_ticket_update", incident_ticket_update)

builder.add_edge(START, "log_extraction")
builder.add_edge("log_extraction", "root_cause_analysis")
builder.add_edge("root_cause_analysis", "incident_ticket_creation")
builder.add_edge("incident_ticket_creation", "solution_agent")
builder.add_edge("solution_agent", "incident_ticket_update")
builder.add_edge("incident_ticket_update", END)

app = builder.compile()


# ---------------- Test ----------------
if __name__ == "__main__":
    output = app.invoke({
        "raw_log": "2024-06-01 12:00:00 ERROR [Producer clientId=producer-1] Failed to send message to topic 'test-topic' partition 0 due to timeout."
    })

    print("\n" + "="*50)
    print("=== Extracted Info ===")
    print(output.get("extracted_info", "N/A"))
    
    print("\n=== Root Cause ===")
    print(output.get("root_cause", "N/A"))
    
    print("\n=== Solution ===")
    print(output.get("solution", "N/A"))
    
    print("\n=== Ticket Info ===")
    print(f"Number : {output.get('ticket_number')}")
    print(f"Sys ID : {output.get('ticket_sys_id')}")
    print(f"URL    : {output.get('ticket_url')}")
    
    print("\n=== Update Status ===")
    print(output.get("updated_ticket", "N/A"))