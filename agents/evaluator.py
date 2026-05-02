from src.llm import get_llm

def evaluator_node(state):

    llm=get_llm()

    prompt=f"""
    You are a strict CloudOps incident review evaluator.

Evaluate whether the diagnosis and fix are good enough.

Incident:
{state["Incident_text"]}

Log Summary:
{state["log_summary"]}

Root Cause:
{state["root_cause"]}

Fix:
{state["fix"]}

Check:
1. Is the root cause supported by evidence?
2. Is the fix specific and actionable?
3. Is there hallucination risk?
4. Is anything important missing?

Return exactly in this format:

STATUS: pass or fail
FEEDBACK: short explanation
"""
    response=llm.invoke(prompt)
    content=response.content.strip() # type: ignore

    status="pass" if "status: pass" in content.lower() else "fail"

    return{ "eval_status": status,
        "eval_feedback": content,
        "node_history": state["node_history"] + ["evaluator_node"]}
