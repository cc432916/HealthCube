# backend.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from ai_planner import router as ai_planner_router
from user_data import router as user_data_router
from llm_image_calorie import router as food_ai_router


app = FastAPI(title="健康魔方 Backend")

# CORS，方便前端用 http://localhost:5173 等域名访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # 开发阶段先放开，正式环境可以改成你的前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载各模块路由
app.include_router(user_data_router)
app.include_router(ai_planner_router)
app.include_router(food_ai_router)


# 直接把 health-cube.html 当首页返回（可选）
@app.get("/", response_class=HTMLResponse)
def index():
    with open("health-cube.html", "r", encoding="utf-8") as f:
        return f.read()
