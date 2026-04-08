from autogen import AssistantAgent, UserProxyAgent
from app.ai.config import get_llm_config
from app.ai.prompts import LEAD_DESIGNER_SYSTEM_PROMPT, NARRATIVE_DESIGNER_PROMP


def create_designer_agent() -> AssistantAgent:
    return AssistantAgent( 
        name = "Lead_Game_Designer",
        system_message = LEAD_DESIGNER_SYSTEM_PROMPT,
        llm_config = get_llm_config(temperature=0.2),
    )


def create_narrative_designer() -> AssistantAgent:
    return AssistantAgent( 
        name = "narrative_designer",
        system_message = NARRATIVE_DESIGNER_PROMP,
        llm_config = get_llm_config(temperature=0.2),
    )


def create_user_proxy() -> UserProxyAgent:
    return UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
        code_execution_config=False
    )