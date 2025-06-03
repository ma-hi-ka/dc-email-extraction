from pydantic import BaseModel, Field, computed_field
from typing import Optional, List, Literal
from datetime import date

class FinancialMetrics(BaseModel):
    mrr: Optional[float] = Field(None, description = "Monthly Recurring Revenue in USD")
    arr: Optional[float] = Field(None, description = "Annual Recurring Revenue in USD")
    revenue: Optional[float] = Field(None, description="Monthly revenue (not derived from MRR)")
    burn_rate: Optional[float] = Field(None, description="Monthly net burn in USD")
    cash_on_hand: Optional[float] = Field(None, description="Cash on Hand in USD")
    runway: Optional[float] = Field(None, description="Runway in Months")
    gross_margin: Optional[float] = Field(None, description="Gross Margin (%)")
    
class CustomerMetrics(BaseModel):
    active_customers: Optional[int] = Field(None, description="Number of Active Customers")
    churn_rate: Optional[float] = Field(None, description="Churn Rate (%)")
    new_customers: Optional[int] = Field(None, description="Number of New Customers")
    usage_stats: Optional[str] = Field(None, description="Usage Notes and Statistics–Product Feedback")

class SalesMetrics(BaseModel):
    mom_revenue_growth: Optional[float] = Field(None, description="MoM Revenue Growth in USD")
    yoy_revenue_growth: Optional[float] = Field(None, description="YoY Revenue Growth in USD")
    backlog_revenue: Optional[float] = Field(None, description="Backlog Revenue in USD")
    target_revenue: Optional[float] = Field(None, description="Targeted Revenue Goal in USD")

class TeamAndOpsMetrics(BaseModel):
    team_size: Optional[int] = Field(None, description="Current Team Size")
    new_hires: Optional[List[str]] = Field([], description="New Roles Hired")
    required_hires: Optional[List[str]] = Field([], description="Required Roles to Hire")
    operation_notes: Optional[str] = Field(None, description="Office/Operations Optimization Notes")
    #e.g. cost cutting measures, support outsourcing

class ProductMilestone(BaseModel):
    description: str = Field(..., description="Major Product/Feature Rollouts")
    event_type: Optional[Literal["Launch", "Upgrade", "Integration", "Partnership", 
                                 "Churn", "Hiring"]] = Field(None)
    integration: Optional[List[str]] = Field([], description="List of integrations")  
    # e.g., 'Launch', 'Upgrade', 'Integration'
    impact: Optional[str] = Field(None, description="Qualitative impact summary")

class CompanyLowLight(BaseModel):
    description: str = Field(..., description="What Went Wrong/Challenge Faced")
    impact: str = Field(..., description="Qualitative Summary Of Challenges' impact")
    possible_causes: Optional[List[str]] = Field([], 
                                                 description="Potential Causes For Lowlight")
    future_changes: Optional[str] = Field(None, 
                                          description="Planned Changes To Address Challenge")


class FundraisingRound(BaseModel):
    round_type: Optional[str] = Field(None, description="Round Type")
    amount_raised: Optional[float] = Field(None, description="Amount Raised in USD")
    amount_remaining: Optional[float] = Field(None, description="Remaining Amount to Raise in USD")
    strategic_investors: Optional[List[str]] = Field([], 
                                                     description="List of Successful Strategic Investors")
    advisors: Optional[List[str]] = Field([], description="List of Effective Advisors")

class CompanyEvent(BaseModel):
    event_type: str
    description: str

class CompanySnapshot(BaseModel):
    company_name: str = Field(description="Company Name")
    year: int = Field(description="Year")
    quarter: int = Field(description="Fiscal Quarter")
    industry: Optional[str] = Field(None, description="Company Industry")
    region: Optional[str] = Field(None, description="Company's Operational Region")
    
    financials: Optional[FinancialMetrics] = Field(None, description="Company's Financial Data")
    customers: Optional[CustomerMetrics] = Field(None, description="Company's Customer Data")
    sales: Optional[SalesMetrics] = Field(None, description="Company's Sales Growth Data")
    team: Optional[TeamAndOpsMetrics] = Field(None, 
                                              description="Company's Office and Operation Data")
    fundraising: Optional[List[FundraisingRound]] = Field([], 
                                                          description="Company's Fundraising Data")
    product_updates: Optional[List[ProductMilestone]] = Field([], 
                                                              description="Company's Product Milestone Data")
    events: Optional[List[CompanyEvent]] = Field([], 
                                                 description="Timeline of Major Company Events")
    
    company_lowlights: Optional[List[CompanyLowLight]] = Field([], description="Challenges, setbacks, and negative events")

    notes: Optional[str] = Field(None, description="Additional Notes")
    source: Optional[str] = Field(None, description= "PDF or Email Source References")