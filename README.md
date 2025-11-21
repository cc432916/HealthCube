# 健康魔方 - AI智能健康管理平台
**HealthCube: AI-driven Personalized Nutrition & Lifestyle Management**

> 基于大语言模型的完整健康管理系统，提供AI饮食计划、运动计划、食物识别和身体数据管理的健康管理平台1.0已经发布，AI视觉卡路里识别、手表体重秤等硬件设备对接功能开发中...

<details>
  <summary>本项目由李蒂澄、原薪璐开发。</summary>

本项目是一个开源项目，项目成员均在 DataWhale 等开源社区招募。

原薪璐[Xinlu Yuan@SenseTime](https://github.com/yuanxinlu-121) 

李蒂澄[Dicheng Li@SenseTime](https://github.com/cc432916) 

</details>

---
## 🎯 项目背景（Project Background）

随着肥胖、代谢综合征等慢性疾病的普遍化，**“如何在日常生活中进行可持续的营养管理”**成为一个重要问题。传统的饮食记录方式依赖人工估算和手动录入，不仅耗时、易遗漏，而且难以给出个性化的综合建议。

**健康魔方（HealthCube）**面向普通体重管理人群、健身人群以及慢病高风险人群，采用大模型（LLM）+ 知识库的技术路线，将：

- **饮食图像识别与卡路里估算**
- **个性化膳食与运动规划**
- **体重与身体成分数据可视化**

集成到一个统一的交互界面中，构建出一个可用于比赛展示与后续科研扩展的**AI智能营养管理原型系统**。

---

## ✨ 核心功能（Key Features）

1. ### 🍽️ AI 饮食记录与建议
   - 用户上传食物图片或自然语言（例如：晚餐吃了一份牛肉土豆和一瓶东方树叶普洱茶），由后端的 `llm_image_calorie.py` 调用大模型，完成：
     - 食物种类识别
     - 单次摄入热量估算
     - 根据健康目标给出“本餐建议”（例如：是否偏油、碳水是否过高等）
   - 结果回显在前端「AI饮食记录与建议」卡片中，可记录到当日饮食。

2. ### 🏃 个性化营养与运动规划
   - 基于 `ai_planner.py`，综合用户的：
     - 身高、体重、BMI、体脂率（`user_body_data.json`）
     - 健康目标（减脂 / 增肌 / 维持）
     - 饮食偏好与禁忌
   - 自动生成每日：
     - 推荐总摄入能量与三大营养素配比
     - 三餐结构建议
     - 运动类型与时长建议

3. ### 📊 体征与饮食数据管理
   - 使用 `user_data.py`、`food_data.py` 管理用户信息与食物营养数据。
   - 通过前端 `health-cube.html` 的图表（基于 Chart.js）展示：
     - 体重变化趋势
     - 每日卡路里收支
     - 一周运动记录等可视化结果。

4. ### 🤖 数据可视化与交互仪表盘
   - 前端以「健康魔方」风格的侧边栏 + 主视图布局，支持：
     - 数据概览
     - 身体数据
     - 食谱推荐
     - 运动计划
     - AI 饮食记录与建议

---

## 📋 系统架构（System Architecture）

本项目采用**前后端分离 + 大模型服务 + 轻量级数据存储**的三层架构：

```text
┌────────────────────────────────────────────────────────┐
│                      前端展示层（Web UI）              │
│   - health-cube.html                                  │
│   - Vite / 原生 JS / Chart.js                         │
│   用户登录、数据概览、饮食记录、AI 建议可视化          │
└───────────────▲───────────────────────┬───────────────┘
                │HTTP / JSON           │
                │                      │
┌───────────────┴──────────────────────▼───────────────┐
│                    后端服务层（Python）               │
│   - backend.py / app.py                               │
│   - ai_planner.py                                     │
│   - llm_image_calorie.py                              │
│   - llm_utils.py                                      │
│   提供统一的 /api/ 接口：                             │
│     • 体征数据读写                                    │
│     • 图片卡路里识别                                  │
│     • AI 饮食与运动规划                               │
└───────────────▲───────────────────────┬───────────────┘
                │调用 SDK / HTTP API   │读写
                │                      │
┌───────────────┴──────────────┐  ┌────┴────────────────┐
│      大模型与外部服务         │  │     数据与配置层     │
│   - 云端/本地 LLM（通过       │  │  - user_body_data.json │
│     llm_utils.py 统一封装）   │  │  - food_data.py        │
│                              │  │  - user_data.py        │
└──────────────────────────────┘  └───────────────────────┘
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install fastapi uvicorn openai python-dotenv pydantic requests
```

### 2. 配置环境

确保 `.env` 文件包含：
```env
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL_NAME=qwen-max
```

### 3. 启动服务

**Windows 用户**:
```bash
启动服务.bat
```

**命令行**:
```bash
python app.py
```

### 4. 访问应用

- **网页页面** : `http://localhost:8000/health-cube.html` ⭐

---

## 📄 许可证

MIT License

## 👥 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 技术支持

- **完整文档**: 查看项目中的 `.md` 文件
- **问题反馈**: GitHub Issues/邮箱

---

**项目版本**: v1.0.0  
**完成时间**: 2025-11-20  
**状态**: ✅ 完整集成完成

**享受健康生活，从智能规划开始！** 🥗💪🏃‍♂️🤖
