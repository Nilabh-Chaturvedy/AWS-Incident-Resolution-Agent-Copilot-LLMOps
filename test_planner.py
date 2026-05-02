from agents.planner import planner_node

state = {
    "Incident_text": "ECS Fargate task is running but Streamlit app not loading.",
    "node_history": []
}

result = planner_node(state)

print(result["plan"])
print(result["node_history"])