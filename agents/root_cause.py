from src.llm import get_llm

def root_cause_node(state):

    llm=get_llm()
    diagnostic_plan=state['plan']
    log_summary=state['log_summary']

    prompt=f"""
 You are a senior Cloud Solutions Architect who can diagnose production failures.
 Based on the following Diagnostic Plan and log summary identify the most likely root cause.

 Diagnostic Plan : {diagnostic_plan}
 Log Summary : {log_summary}

Return:
1. Most likely root cause
2. Confidence: Low / Medium / High
3. Supporting evidence
4. Alternative causes
"""
    response=llm.invoke(prompt)

    return{
        'root_cause':response.content,
        'retry_count':state['retry_count']+1,
        'node_history':state['node_history']+['root_cause_node']
    }