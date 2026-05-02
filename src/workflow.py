from langgraph.graph import StateGraph,START,END
from src.state import OPSPilotState
from agents.planner import planner_node
from agents.log_analyzer import log_analyzer_node
from agents.root_cause import root_cause_node
from agents.fix_generator import fix_generator_node
from agents.reporter import reporter_node
from agents.router import router_node
from agents.ecs_diagnostics import ecs_diagnostics_node
from agents.evaluator import evaluator_node


def route_after_router(state):

    category=state["incident_type"]
    if category == "ecs":
        return "ecs_diagnostics"

    elif category == "docker":
        return "log_analyzer"

    elif category == "network":
        return "log_analyzer"

    else:
        return "planner"

def evaluator(state):

    if state["eval_status"]=="pass":
        return "reporter"
    
    if state["retry_count"]>=1:
        return "reporter"
    
    else:
        return "root_cause"


def build_graph():
    
    builder=StateGraph(OPSPilotState) #Builder builds the stategraph with state dictionary as input param

    builder.add_node("planner",planner_node) #Adds a node
    builder.add_node("log_analyzer",log_analyzer_node)
    builder.add_node("root_cause",root_cause_node)
    builder.add_node("fix_generator",fix_generator_node)
    builder.add_node("reporter",reporter_node)
    builder.add_node("router",router_node)
    builder.add_node("ecs_diagnostics",ecs_diagnostics_node)
    builder.add_node("evaluator",evaluator_node)
    builder.set_entry_point("router") #Sets entry point of workflow as the router node
    builder.add_conditional_edges("router",
                                  route_after_router,
                                  {
                                      "planner":"planner",
                                      "ecs_diagnostics":"ecs_diagnostics",
                                      "log_analyzer":"log_analyzer"})
    builder.add_edge("planner","log_analyzer") #Add edges in the Langgraph flow
    builder.add_edge("log_analyzer","root_cause")
    builder.add_edge("ecs_diagnostics","root_cause")
    builder.add_edge("root_cause","fix_generator")
    builder.add_edge("fix_generator","evaluator")
    builder.add_conditional_edges(
    "evaluator",
    evaluator,
    {
        "reporter": "reporter",
        "root_cause" : "root_cause"
    }

    )
    builder.add_edge("reporter",END)
    
    return builder.compile()  #Returns the executable flow




