from src.llm import get_llm


def planner_node(state):
    llm = get_llm()

    incident = state["Incident_text"]

    prompt = f"""
You are a senior CloudOps engineer.

A production issue has occurred:

{incident}

Create a concise investigation plan with 4 bullet points.
Focus on AWS ECS / Docker / networking / logs.
"""

    response = llm.invoke(prompt)

    return {
        "plan": response.content,
        "node_history": state["node_history"] + ["planner_node"]
    }