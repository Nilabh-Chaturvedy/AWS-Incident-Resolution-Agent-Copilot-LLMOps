from src.llm import get_llm

def reporter_node(state):

    llm=get_llm()

    prompt=f"""
You are an engineering incident manager.

Create a concise final incident report using the information below.

Incident:
{state["Incident_text"]}

Plan:
{state["plan"]}

Log Summary:
{state["log_summary"]}

Root Cause:
{state["root_cause"]}

Fix Recommendation:
{state["fix"]}

Return in this format:

1. Executive Summary
2. Root Cause
3. Immediate Actions
4. Prevention Steps
5. Severity (Low/Medium/High/Critical)
"""
    response=llm.invoke(prompt)

    return {
        "final_report":response.content,
        "node_history": state["node_history"] + ["reporter_node"]
}
