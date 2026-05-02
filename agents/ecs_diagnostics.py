from src.llm import get_llm


def ecs_diagnostics_node(state):
    llm = get_llm()

    prompt = f"""
You are an AWS ECS/Fargate diagnostics expert.

Analyze this ECS/Fargate incident:

{state["Incident_text"]}

Focus specifically on:
1. ECS service status
2. Task stopped reasons
3. Container port mappings
4. Security groups
5. ALB target group health checks
6. Task definition CPU/memory
7. Environment variables and secrets
8. CloudWatch logs

Return:
- ECS-specific diagnostic checklist
- Most suspicious ECS components
- Evidence to look for
"""

    response = llm.invoke(prompt)

    return {
        "log_summary": response.content,
        "node_history": state["node_history"] + ["ecs_diagnostics_node"]
    }