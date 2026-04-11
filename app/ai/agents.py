from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel
import httpx
from typing import List, Dict, Any

from app.ai.prompts import ROUTER_PROMPT, LEAD_GAME_DESIGNER_PROMPT, NARRATIVE_DESIGNER_PROMPT, CORE_MECHANICS_DESIGNER_PROMPT, ECONOMY_AND_MONETIZATION_DESIGNER_PROMPT, MARKET_ANALYST_PROMPT, TECHNICAL_PRODUCER_PROMPT
from app.ai.config import flash_model, pro_model
from app.schemas.agents import RouterOutput


router_agent = Agent(
    flash_model, 
    output_type=RouterOutput, 
    system_prompt=ROUTER_PROMPT
)


narrative_agent = Agent(
    flash_model, 
    system_prompt=NARRATIVE_DESIGNER_PROMPT
)


mechanics_agent = Agent(
    flash_model, 
    system_prompt=CORE_MECHANICS_DESIGNER_PROMPT,
)


economy_agent = Agent(
    flash_model, 
    system_prompt=ECONOMY_AND_MONETIZATION_DESIGNER_PROMPT
)


market_agent = Agent(
    flash_model, 
    system_prompt=MARKET_ANALYST_PROMPT
)

@market_agent.tool
async def fetch_steam_market_data(ctx: RunContext[None], genre: str, tags: List[str]) -> Dict[str, Any]:
    url = "https://steamspy.com/api.php"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params={"request": "tag", "tag": genre})
        
        if response.status_code != 200:
            return {"error": "Failed to fetch data from SteamSpy API"}
            
        data = response.json()
        games = list(data.values())[:15]
        
        market_sample = []
        for game in games:
            market_sample.append({
                "name": game.get("name"),
                "ccu": game.get("ccu"),
                "positive_reviews": game.get("positive"),
                "negative_reviews": game.get("negative"),
                "price": game.get("price", 0) / 100 
            })
            
        return {
            "requested_genre": genre,
            "top_games_sample": market_sample
        }


tech_agent = Agent(
    flash_model, 
    system_prompt=TECHNICAL_PRODUCER_PROMPT
)


lead_agent = Agent(
    pro_model, 
    system_prompt=LEAD_GAME_DESIGNER_PROMPT
)
