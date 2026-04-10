import json
from app.ai.agents import (router_agent, narrative_agent, mechanics_agent,
                           economy_agent, market_agent, tech_agent, lead_agent)


async def run_specialist(agent: Agent, chunk: str, role_name: str) -> tuple[str, str]:
    result = await agent.run(chunk)
    return role_name, result.data


async def analyze_gdd(text: str) -> dict:
    router_result = await router_agent.run(gdd_text)
    routing_data = router_result.data

    if not routing_data.is_valid_gdd or not routing_data.chunks:
        return f"Ошибка валидации GDD: {routing_data.error_message}"

    tasks = []
    chunks = routing_data.chunks

    if chunks.narrative_chunk:
        tasks.append(run_specialist(narrative_agent, chunks.narrative_chunk, "Narrative"))
    if chunks.core_mechanics_chunk:
        tasks.append(run_specialist(mechanics_agent, chunks.core_mechanics_chunk, "Mechanics"))
    if chunks.economy_monetization_chunk:
        tasks.append(run_specialist(economy_agent, chunks.economy_monetization_chunk, "Economy"))
    if chunks.market_analyst_chunk:
        tasks.append(run_specialist(market_agent, chunks.market_analyst_chunk, "Market"))
    if chunks.technical_producer_chunk:
        tasks.append(run_specialist(tech_agent, chunks.technical_producer_chunk, "Tech"))

    specialist_results = await asyncio.gather(*tasks)

    compiled_reports = "\n\n".join([f"--- ОТЧЕТ {role.upper()} ---\n{report}" for role, report in specialist_results])

    lead_result = await lead_agent.run(compiled_reports)
    return lead_result.data
