from pydantic import BaseModel, Field
from typing import List

class CodeIssue(BaseModel):
    category: str = Field(description="One of: Bug, Security, Quality, Performance")
    severity: str = Field(description="One of: Critical, High, Medium, Low, Suggestion")
    title: str = Field(description="Short title of the issue")
    line: str = Field(description="Line number(s) or function name")
    explanation: str = Field(description="What is wrong and why it is a problem")
    recommendation: str = Field(description="How to fix it")

class IssueList(BaseModel):
    issues: List[CodeIssue]

class ImprovedCodeResult(BaseModel):
    improved_code: str = Field(description="The refactored and improved source code")

class FinalReviewResult(BaseModel):
    overall_score: int = Field(description="Score from 0 to 100")
    risk_level: str = Field(description="Safe, Low, Medium, High, or Critical")
    summary: str = Field(description="Brief summary of the code state")
    main_problems: List[str] = Field(description="List of top 3-5 main problems")
    top_recommendations: List[str] = Field(description="List of top 3-5 recommendations")