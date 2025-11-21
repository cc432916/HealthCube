from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from llm_utils import call_llm, parse_json_from_llm

router = APIRouter(prefix="/api/ai", tags=["ai-planner"])


# ========= 数据模型 =========

class BodyProfile(BaseModel):
    gender: str = Field(..., description="male / female")
    age: int
    height: float = Field(..., description="cm")
    weight: float = Field(..., description="kg")
    bmi: Optional[float] = None
    body_fat: Optional[float] = Field(None, description="体脂率 %")
    waist: Optional[float] = None
    hip: Optional[float] = None
    whr: Optional[float] = None
    activity_level: Optional[str] = None  # sedentary / light / moderate / active / athlete


class DietPreferences(BaseModel):
    goal: str = Field(..., description="lose / gain / maintain")
    calories_budget: int
    diet_type: str = "none"          # none / vegetarian / vegan / low-carb ...
    restrictions: List[str] = []
    tastes: List[str] = []


class MealItem(BaseModel):
    meal_type: str     # 早餐 / 午餐 / 晚餐 / 加餐
    name: str
    calories: int
    tags: List[str] = []
    description: str
    suggestion: str


class MealPlanRequest(BaseModel):
    profile: BodyProfile
    preferences: DietPreferences


class MealPlanResponse(BaseModel):
    daily_calorie_target: int
    goal: str
    meals: List[MealItem]


class WorkoutPreferences(BaseModel):
    goal: str = Field(..., description="lose / gain / maintain / health")
    available_minutes: int
    frequency_per_week: int
    equipment: List[str] = []
    limitations: List[str] = []      # 例如 ["knee_pain"]


class WorkoutSession(BaseModel):
    name: str
    type: str                # cardio / strength / hiit / yoga / mobility
    duration_minutes: int
    intensity: str           # low / medium / high
    target_heart_rate: Optional[str] = None
    description: str
    exercises: List[str]
    tips: str


class WorkoutPlanRequest(BaseModel):
    profile: BodyProfile
    preferences: WorkoutPreferences


class WorkoutPlanResponse(BaseModel):
    day: str
    goal: str
    total_duration: int
    sessions: List[WorkoutSession]


FOOD_SHORT_TABLE = """
以下是一些常见食物的大致热量信息（每 100g 或一份）：
- 燕麦片: 389 kcal
- 鸡胸肉: 165 kcal
- 三文鱼: 208 kcal
- 鸡蛋: 155 kcal
- 牛油果: 160 kcal
- 西兰花: 34 kcal
- 西红柿: 18 kcal
- 糙米饭: 111 kcal
- 苹果: 52 kcal
- 香蕉: 89 kcal
- 希腊酸奶: 59 kcal
- 豆腐: 76 kcal
- 虾仁: 99 kcal
- 土豆: 77 kcal
- 西兰花炒鸡胸（家常做法，一份约）: 260-320 kcal
- 鸡胸肉沙拉（去皮）: 250-350 kcal
"""


# ========= 食谱推荐 =========

@router.post("/meal-plan", response_model=MealPlanResponse)
def generate_meal_plan(req: MealPlanRequest):
    profile = req.profile
    prefs = req.preferences

    system_prompt = (
        "你是一名专业的运动营养师，请为用户规划一整天的饮食方案（早餐、午餐、晚餐、加餐）。"
        "必须用 JSON 返回：daily_calorie_target, goal, meals。"
        "meals 数组中每个元素包含：meal_type, name, calories, tags, description, suggestion。"
        "meal_type 只能是 '早餐'、'午餐'、'晚餐'、'加餐'。"
        "calories 为整数 kcal。"
        "输出必须是可被 json.loads 解析的『纯 JSON』，不能带解释性文字。"
    )

    user_prompt = f"""
用户基本信息：
- 性别: {profile.gender}
- 年龄: {profile.age}
- 身高: {profile.height} cm
- 体重: {profile.weight} kg
- BMI: {profile.bmi or '-'}
- 体脂率: {profile.body_fat or '-'} %
- 腰围: {profile.waist or '-'} cm
- 臀围: {profile.hip or '-'} cm
- 腰臀比: {profile.whr or '-'}
- 日常活动水平: {profile.activity_level or '未说明'}

饮食目标与偏好：
- 目标: {prefs.goal} (lose=减脂, gain=增肌, maintain=维持)
- 每日热量预算: {prefs.calories_budget} kcal
- 饮食类型: {prefs.diet_type}
- 饮食禁忌: {', '.join(prefs.restrictions) if prefs.restrictions else '无'}
- 口味偏好: {', '.join(prefs.tastes) if prefs.tastes else '无'}

要求：
1. 必须包含 早餐、午餐、晚餐、加餐 四顿。
2. 总热量尽量接近用户预算。
3. 优先使用下面表格里的常见食材，便于用户估算：

{FOOD_SHORT_TABLE}

4. 避开饮食禁忌，考虑饮食类型（素食等）。
"""

    try:
        raw = call_llm(system_prompt, user_prompt)
        data = parse_json_from_llm(raw)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM 调用失败: {e}")

    meals: List[MealItem] = []
    for m in data.get("meals", []):
        meals.append(
            MealItem(
                meal_type=m.get("meal_type", "早餐"),
                name=m.get("name", "健康餐"),
                calories=int(m.get("calories", prefs.calories_budget // 4)),
                tags=m.get("tags", []),
                description=m.get("description", ""),
                suggestion=m.get("suggestion", ""),
            )
        )

    return MealPlanResponse(
        daily_calorie_target=int(data.get("daily_calorie_target", prefs.calories_budget)),
        goal=data.get("goal", prefs.goal),
        meals=meals,
    )


# ========= 运动计划 =========

@router.post("/workout-plan", response_model=WorkoutPlanResponse)
def generate_workout_plan(req: WorkoutPlanRequest):
    profile = req.profile
    prefs = req.preferences

    system_prompt = (
        "你是一名资深体能教练，请为用户规划『今天的一次训练』。"
        "训练由 2-4 个 session 组成，例如：热身、主训练、辅助训练、拉伸。"
        "必须返回 JSON：day, goal, total_duration, sessions。"
        "sessions 中每个元素包含："
        "name, type, duration_minutes, intensity, target_heart_rate, description, exercises, tips。"
        "type 只能是 cardio / strength / hiit / yoga / mobility 等。"
        "intensity 只能是 low / medium / high。"
        "输出必须是纯 JSON。"
    )

    user_prompt = f"""
用户基本信息：
- 性别: {profile.gender}
- 年龄: {profile.age}
- 身高: {profile.height} cm
- 体重: {profile.weight} kg
- BMI: {profile.bmi or '-'}
- 体脂率: {profile.body_fat or '-'} %
- 日常活动水平: {profile.activity_level or '未说明'}

训练目标与限制：
- 当前训练目标: {prefs.goal}
- 计划每周训练天数: {prefs.frequency_per_week} 天
- 今天可用训练时间: {prefs.available_minutes} 分钟
- 可用器械: {', '.join(prefs.equipment) if prefs.equipment else '无器械，仅徒手'}
- 身体限制 / 伤病: {', '.join(prefs.limitations) if prefs.limitations else '无'}

要求：
1. 总训练时长不要超过用户可用时间。
2. 如有膝盖/腰部等伤病，避免高冲击动作，并在 tips 中提醒。
3. 每个 session 给出 3-6 个具体动作名称。
4. target_heart_rate 用区间字符串表示，例如 "120-140 bpm"。
"""

    try:
        raw = call_llm(system_prompt, user_prompt)
        data = parse_json_from_llm(raw)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM 调用失败: {e}")

    sessions: List[WorkoutSession] = []
    total_duration = 0

    for s in data.get("sessions", []):
        duration = int(s.get("duration_minutes", prefs.available_minutes // 3))
        total_duration += duration
        sessions.append(
            WorkoutSession(
                name=s.get("name", "训练小节"),
                type=s.get("type", "cardio"),
                duration_minutes=duration,
                intensity=s.get("intensity", "medium"),
                target_heart_rate=s.get("target_heart_rate"),
                description=s.get("description", ""),
                exercises=s.get("exercises", []),
                tips=s.get("tips", ""),
            )
        )

    total_duration = int(data.get("total_duration", total_duration))

    return WorkoutPlanResponse(
        day=data.get("day", "今天"),
        goal=data.get("goal", prefs.goal),
        total_duration=total_duration,
        sessions=sessions,
    )
