from src.llm import get_llm

def fix_generator_node(state):
    
    llm=get_llm()

    prompt=f"""
    You are a Senior Cloud Solution Architect with AWS specialization and
    are expert on DEVOPS/MLOPS issues.Based on the incident analysis below, generate practical remediation steps.

Incident:
{state["Incident_text"]}

Root cause:
{state["root_cause"]}

Return:
1. Immediate fix
2. AWS CLI command if applicable
3. Docker/ECS config change if applicable
4. Prevention recommendation
5. Human approval needed? yes/no
"""
    response=llm.invoke(prompt)

    return{

        "fix":response.content,
        "node_history":state['node_history']+['fix_generator_node']

    }