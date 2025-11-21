# llm_image_calorie.py
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from food_data import FOOD_CALORIE_TABLE
from llm_utils import call_llm, parse_json_from_llm

router = APIRouter(prefix="/api/ai", tags=["ai-food"])


class FoodCalorieRequest(BaseModel):
    query: str = "一份鸡胸肉沙拉，大概 200g"
    # 以后要接图片，可以再加 image_url / image_base64 字段


class FoodCalorieResponse(BaseModel):
    name: str
    calories: int
    health_score: int     # 1-5
    advice: str
    matched_from_table: bool = False


@router.post("/food-calorie", response_model=FoodCalorieResponse)
def estimate_food_calorie(req: FoodCalorieRequest):
    table_text = "\n".join(
        [f"- {name}: {kcal} kcal" for name, kcal in FOOD_CALORIE_TABLE.items()]
    )

    system_prompt = (
        "你是一名专业营养师，擅长根据食物描述估算热量。"
        "你会优先在给出的食物热量表中找到最接近的食物，然后结合分量估算总热量。"
        "必须以 JSON 形式回答："
        '{"name": 食物名称, "calories": 估算总热量整数kcal, '
        '"health_score": 1到5的整数评分, "advice": "一句中文建议", '
        '"matched_from_table": true/false}。'
        "不要输出任何解释性文字。"
    )

    user_prompt = f"""
用户描述的食物：{req.query}

可参考的食物热量表（每 100g 或每份）：
{table_text}
"""

    try:
        raw = call_llm(system_prompt, user_prompt)
        data = parse_json_from_llm(raw)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM 调用失败: {e}")

    return FoodCalorieResponse(
        name=data.get("name", "未识别食物"),
        calories=int(data.get("calories", 300)),
        health_score=int(data.get("health_score", 3)),
        advice=data.get("advice", "注意控制总热量和油脂摄入。"),
        matched_from_table=bool(data.get("matched_from_table", False)),
    )
