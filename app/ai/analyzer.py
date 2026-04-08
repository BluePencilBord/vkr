import json
from app.ai.agents import create_designer_agent, create_user_proxy


async def analyze_gdd(text: str) -> dict:
    designer_agent = create_designer_agent()
    user_proxy = create_user_proxy()

    task_prompt = f"Проанализируй следующий геймдизайн-документ и верни JSON-отчет:\n\n{text}"

    chat_result = await user_proxy.a_initiate_chat(
        designer_agent,
        message=task_prompt,
        summary_method="last_msg"
    )

    try:
        response_text = chat_result.summary
        return json.loads(response_text)
    except Exception as e:
        return {
            "error": "Агент не вернул валидный JSON", 
            "raw_response": str(chat_result.summary) if chat_result else str(e)
        }
