from typing import TypedDict, List
from schemas import CodeIssue

class CodeReviewState(TypedDict):
    code: str
    language: str
    error: str
    
    # Agent Results
    bugs: List[CodeIssue]
    security_issues: List[CodeIssue]
    quality_issues: List[CodeIssue]
    performance_issues: List[CodeIssue]
    
    # Aggregated & Final
    combined_issues: List[CodeIssue]
    improved_code: str
    final_review: dict  # Holds score, risk, summary, etc.