from typing import TypedDict,List,Optional,Any,Dict

class OPSPilotState(TypedDict):
    #Input
    Incident_text: str
    user_question: Optional[str]

    #Workflow Memory 
    messages : List[Dict[str,str]]
    memory: Dict[str,Any]

    #Agent Output

    plan : Optional[List[str]]
    log_summary : Optional[str]
    root_cause : Optional[str]
    fix : Optional[str]
    final_report : Optional[str]

    #RAG/Evidence

    retrieved_docs : Optional[List[Dict[str,Any]]]
    evidence : Optional[List[str]]

    #Evaluation 

    eval_score : Optional[float]
    eval_notes : Optional[str]
    hallucination_risk : Optional[str]

    # Observability / tracing
    trace_id: Optional[str]
    node_history: List[str]
    errors: List[str]

    # Human approval / safety
    needs_human_review: bool
    approved_action: Optional[bool]

    #Routing Incidence
    incident_type : Optional[str]
    routing_reason : Optional[str]

    #Evaluation
    eval_status: Optional[str]
    eval_feedback: Optional[str]
    retry_count:int



