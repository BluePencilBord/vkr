from pydantic_ai import Agent
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool

from app.ai.prompts import (
    ROUTER_PROMPT, 
    NARRATIVE_DESIGNER_PROMPT, 
    CORE_MECHANICS_DESIGNER_PROMPT, 
    ECONOMY_AND_MONETIZATION_DESIGNER_PROMPT, 
    MARKET_ANALYST_PROMPT, 
    TECHNICAL_PRODUCER_PROMPT,
    LEAD_GAME_DESIGNER_PROMPT
)
from app.ai.config import model
from app.schemas.agents import RouterOutput, LeadDesignerOutput
from app.ai.agent_tools import fetch_steam_market_data, calculate_formula

router_agent = Agent(
    model, 
    output_type=RouterOutput, 
    system_prompt=ROUTER_PROMPT
)

narrative_agent = Agent(
    model, 
    system_prompt=NARRATIVE_DESIGNER_PROMPT
)

mechanics_agent = Agent(
    model, 
    system_prompt=CORE_MECHANICS_DESIGNER_PROMPT,
    tools=[calculate_formula]
)

economy_agent = Agent(
    model, 
    system_prompt=ECONOMY_AND_MONETIZATION_DESIGNER_PROMPT,
    tools=[calculate_formula]
)

market_agent = Agent(
    model, 
    system_prompt=MARKET_ANALYST_PROMPT,
    tools=[fetch_steam_market_data, duckduckgo_search_tool(max_results=3)]
)

tech_agent = Agent(
    model, 
    system_prompt=TECHNICAL_PRODUCER_PROMPT
)

lead_agent = Agent(
    model,
    system_prompt=LEAD_GAME_DESIGNER_PROMPT,
    output_type=LeadDesignerOutput,
    retries=2
)
