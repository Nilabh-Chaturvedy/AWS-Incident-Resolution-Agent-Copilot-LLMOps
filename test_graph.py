from src.workflow import build_graph

graph=build_graph()

initial_state = {
    "Incident_text": "ECS Fargate task is running but Streamlit app is not loading. Logs show connection refused on port 8501.",
    "user_question": None,
    "messages": [],
    "memory": {},
    "plan": None,
    "log_summary": None,
    "root_cause": None,
    "fix": None,
    "final_report": None,
    "retrieved_docs": None,
    "evidence": None,
    "eval_score": None,
    "eval_notes": None,
    "hallucination_risk": None,
    "trace_id": "test-trace-001",
    "node_history": [],
    "errors": [],
    "needs_human_review": False,
    "approved_action": None,
    "eval_status":None,
    "eval_feedback": None,
    "retry_count":0
}

result=graph.invoke(initial_state)


print("\nIncident Type")
print(result["incident_type"])

print("PLAN :")
print(result['plan'])


print("\nLog Summary:")
print(result["log_summary"])

print("\n Root Cause Summary")
print(result["root_cause"])

print("\n Fix Report")
print(result["fix"])

print("\n Final Report :")
print(result['final_report'])

print("\nNODE HISTORY:")
print(result["node_history"])



