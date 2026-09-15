from langgraph.graph import StateGraph, END
from state import CodeReviewState
from utils.validators import validate_source_code
from agents.bug_analyzer import bug_analyzer_node
from agents.security_analyzer import security_analyzer_node
from agents.quality_analyzer import quality_analyzer_node
from agents.performance_analyzer import performance_analyzer_node
from agents.improvement_agent import improvement_agent_node
from agents.final_reviewer import final_reviewer_node

def validate_code_node(state: dict) -> dict:
    error = validate_source_code(state["code"], state["language"])
    return {"error": error}

def aggregator_node(state: dict) -> dict:
    all_issues = (
        state.get("bugs", []) + 
        state.get("security_issues", []) + 
        state.get("quality_issues", []) + 
        state.get("performance_issues", [])
    )
    
    # 🔴 FIX: Changed i.title to i["title"] and i.line to i["line"]
    unique_issues = {f"{i['title']}-{i['line']}": i for i in all_issues}.values()
    
    severity_rank = {"Critical": 1, "High": 2, "Medium": 3, "Low": 4, "Suggestion": 5}
    
    # 🔴 FIX: Changed x.severity to x["severity"]
    sorted_issues = sorted(unique_issues, key=lambda x: severity_rank.get(x['severity'], 5))
    
    return {"combined_issues": list(sorted_issues)}

def route_after_validation(state: dict):
    if state.get("error"):
        return "END"
    return "analyze"

def build_graph():
    builder = StateGraph(CodeReviewState)

    # Add Nodes
    builder.add_node("validate", validate_code_node)
    
    # We use a sequential flow here for simplicity and safety, 
    # but the architecture is modular enough to map to parallel execution using LangGraph subgraphs or maps.
    builder.add_node("bug_analyzer", bug_analyzer_node)
    builder.add_node("security_analyzer", security_analyzer_node)
    builder.add_node("quality_analyzer", quality_analyzer_node)
    builder.add_node("performance_analyzer", performance_analyzer_node)
    
    builder.add_node("aggregator", aggregator_node)
    builder.add_node("improvement", improvement_agent_node)
    builder.add_node("final", final_reviewer_node)

    # Edges
    builder.set_entry_point("validate")
    
    # Conditional edge: stop if validation fails
    builder.add_conditional_edges(
        "validate",
        route_after_validation,
        {
            "END": END,
            "analyze": "bug_analyzer"
        }
    )
    
    # Sequential analysis sequence
    builder.add_edge("bug_analyzer", "security_analyzer")
    builder.add_edge("security_analyzer", "quality_analyzer")
    builder.add_edge("quality_analyzer", "performance_analyzer")
    builder.add_edge("performance_analyzer", "aggregator")
    builder.add_edge("aggregator", "improvement")
    builder.add_edge("improvement", "final")
    builder.add_edge("final", END)

    return builder.compile()

# Instantiate global graph runner
review_graph = build_graph()