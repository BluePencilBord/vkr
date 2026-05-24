from pydantic_ai import Agent
from pydantic_ai import ModelSettings
import asyncio
import json

from app.ai.agents import (router_agent, narrative_agent, mechanics_agent,
                           economy_agent, market_agent, tech_agent, lead_agent)


async def run_specialist(agent: Agent, chunk: str, role_name: str, update_progress = None) -> tuple[str, str]:
    if update_progress:
        await update_progress(role_name, "running")

    result = await agent.run(chunk)

    if update_progress:
        await update_progress(role_name, "completed")

    return role_name, result.output


async def analyze_gdd(text: str, logger, update_progress = None) -> dict:
    if update_progress:
        await update_progress("Router", "running")

    router_result = await router_agent.run(text)
    routing_data = router_result.output

    if update_progress:
        await update_progress("Router", "completed")

    if not routing_data.is_valid_gdd:
        err_msg = routing_data.error_message or "gdd rejected. no comments from router agent."
        return {"error": f"GDD validation error: {err_msg}"}

    if not routing_data.chunks:
        return {"error": f"GDD validation error: no chunks \n {str(routing_data)}"}

    tasks = []
    chunks = routing_data.chunks

    if chunks.narrative_chunk and chunks.narrative_chunk != 'null':
        tasks.append(run_specialist(narrative_agent, chunks.narrative_chunk, "Narrative", update_progress))
    if chunks.core_mechanics_chunk and chunks.core_mechanics_chunk != 'null':
        tasks.append(run_specialist(mechanics_agent, chunks.core_mechanics_chunk, "Mechanics", update_progress))
    if chunks.economy_monetization_chunk and chunks.economy_monetization_chunk != 'null':
        tasks.append(run_specialist(economy_agent, chunks.economy_monetization_chunk, "Economy", update_progress))
    if chunks.market_analyst_chunk and chunks.market_analyst_chunk != 'null':
        tasks.append(run_specialist(market_agent, chunks.market_analyst_chunk, "Market", update_progress))
    if chunks.technical_producer_chunk and chunks.technical_producer_chunk != 'null':
        tasks.append(run_specialist(tech_agent, chunks.technical_producer_chunk, "Tech", update_progress))

    specialist_results = await asyncio.gather(*tasks)

    compiled_reports = "\n\n".join([f"--- ОТЧЕТ {role.upper()} ---\n{report}" for role, report in specialist_results])
    logger.info(f"Compiled reports generated successfully: \n{compiled_reports}")

    lead_result = await lead_agent.run(compiled_reports, model_settings=ModelSettings(max_tokens=100000))
    return lead_result.output
