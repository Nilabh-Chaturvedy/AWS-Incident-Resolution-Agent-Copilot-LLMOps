from src.llm import get_llm

def router_node(state):

    llm=get_llm()
    incident_text = state.get("Incident_text") or state.get("incident_text")
    if not incident_text:
        raise ValueError("Missing incident text in workflow state.")

    prompt=f"""You are a CloudOps triage router.

Classify this incident into ONE category only:

ecs
docker
network
secrets
memory
kubernetes
application
unknown

Incident:
{incident_text}

Return only the category word.
"""
    response=llm.invoke(prompt)
    incident_type=response.content.strip().lower() # type: ignore

    return{
        "incident_type":incident_type,
        "routing_reason":f"detected category: {incident_type}",
        "node_history":state['node_history']+["router_node"]
        }
