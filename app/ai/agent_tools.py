import ast
import operator
import httpx
from typing import Any, List, Dict
from pydantic_ai import RunContext

ALLOWED_OPERATORS = {
    ast.Add: operator.add, 
    ast.Sub: operator.sub, 
    ast.Mult: operator.mul,
    ast.Div: operator.truediv, 
    ast.Pow: operator.pow, 
    ast.USub: operator.neg
}

def safe_eval(node: ast.AST) -> Any:
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.BinOp):
        return ALLOWED_OPERATORS[type(node.op)](safe_eval(node.left), safe_eval(node.right))
    elif isinstance(node, ast.UnaryOp):
        return ALLOWED_OPERATORS[type(node.op)](safe_eval(node.operand))
    raise TypeError(f"Неподдерживаемая операция: {type(node)}")

async def calculate_formula(ctx: RunContext[None], expression: str) -> str:
    """
    Используй этот инструмент для любых математических вычислений баланса (DPS, время, экономика, вероятности).
    Передавай строго математическое выражение в виде строки. Пример: "100 * (1.5 ** 3)".
    """
    try:
        clean_expr = expression.strip().strip("'\"")
        result = safe_eval(ast.parse(clean_expr, mode='eval').body)
        return f"Результат вычисления: {result}"
    except Exception as e:
        return f"Ошибка вычисления: {str(e)}. Проверь синтаксис формулы, используй только числа и базовые операторы."


async def fetch_steam_market_data(ctx: RunContext[None], genre: str, tags: List[str]) -> Dict[str, Any]:
    """
    Используй этот инструмент для получения информации о рынке в Steam по жанру.
    """
    url = "https://steamspy.com/api.php"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params={"request": "tag", "tag": genre})
        
        if response.status_code != 200:
            return {"error": "Failed to fetch data from SteamSpy API"}
            
        data = response.json()
        games = list(data.values())[:15]
        
        market_sample = []
        for game in games:
            raw_price = game.get("price", 0)
            
            try:
                parsed_price = float(raw_price) / 100
            except (ValueError, TypeError):
                parsed_price = 0.0
            
            market_sample.append({
                "name": game.get("name"),
                "ccu": game.get("ccu"),
                "positive_reviews": game.get("positive"),
                "negative_reviews": game.get("negative"),
                "price": parsed_price
            })
            
        return {
            "requested_genre": genre,
            "top_games_sample": market_sample
        }
