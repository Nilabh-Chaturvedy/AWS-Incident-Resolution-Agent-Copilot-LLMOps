from src.llm import get_llm


def log_analyzer_node(state):
    llm = get_llm()

    incident = state["Incident_text"]

    prompt = f"""
You are a CloudOps log analysis expert.

Analyze the following incident/log text and extract:
1. Key error messages
2. Affected service/component
3. Possible technical signals
4. Missing information needed

Incident/logs:
{incident}

Return a concise structured summary.
"""

    response = llm.invoke(prompt)

    return {
        "log_summary": response.content,
        "node_history": state["node_history"] + ["log_analyzer_node"]
    }