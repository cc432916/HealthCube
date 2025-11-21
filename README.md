# 健康魔方 - AI智能健康管理平台

> 基于大语言模型的完整健康管理系统，提供AI饮食计划、运动计划、食物识别和身体数据管理

**⭐ 所有功能都集成在 health-cube.html 中！**

**📋 [最终确认](最终确认.md)** | **🚀 [快速启动](快速启动指南.md)** | **🧪 [功能测试](功能测试指南.md)** | **🔧 [故障排除](故障排除指南.md)**

**📊 [系统流程图](系统流程图.md)** | **🛣️ [技术路线图](技术路线图.md)**

## 🎯 项目特色

- 🍽️ **AI饮食计划** - 个性化饮食方案生成
- 🏃 **AI运动计划** - 智能运动规划
- 📸 **AI食物识别** - 食物热量智能分析
- 📊 **身体数据管理** - 体重、BMI等数据追踪
- 🤖 **大模型驱动** - 使用通义千问提供智能服务

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

- **AI规划页面** (推荐): `http://localhost:8000/ai-planner-page.html` ⭐
- **原完整系统**: `http://localhost:8000`
- **API文档**: `http://localhost:8000/docs`

## ✨ 核心功能

### 1. AI饮食计划生成
- 输入个人信息和目标
- AI生成完整的一日三餐计划
- 包含热量、营养建议
- 考虑饮食偏好和禁忌

### 2. AI运动计划生成
- 输入身体状况和训练需求
- AI生成个性化运动计划
- 包含具体动作和强度
- 提供安全提示

### 3. AI食物热量识别
- 自然语言描述食物
- AI智能分析热量
- 健康评分（1-5星）
- 专业营养建议

### 4. 身体数据管理
- 记录体重、身高等数据
- 自动计算BMI
- 查看历史记录
- 数据可视化

## 📋 项目结构

```
健康魔方/
├── 后端模块
│   ├── backend.py              # FastAPI主应用
│   ├── ai_planner.py          # AI饮食和运动计划
│   ├── llm_image_calorie.py   # AI食物识别
│   ├── user_data.py           # 身体数据管理
│   ├── llm_utils.py           # LLM工具
│   └── food_data.py           # 食物数据库
├── 前端页面
│   ├── health-cube.html       # 原完整系统
│   └── ai-planner-page.html   # AI规划页面 ⭐
├── 测试工具
│   ├── test_all_modules.py    # 完整测试
│   └── test_ai_diet.py        # 饮食功能测试
└── 文档
    ├── 完整集成文档.md         # 系统集成说明
    ├── 快速启动指南.md         # 快速开始
    └── 项目最终总结.md         # 项目总结
```

## 🧪 测试

### 完整测试
```bash
python test_all_modules.py
```

### 快速测试
```bash
快速测试.bat
```

## 📚 文档导航

### 新手用户
1. [快速启动指南](快速启动指南.md) - 5分钟快速开始
2. [AI饮食功能使用说明](AI饮食功能使用说明.md) - 详细使用指南

### 开发者
1. [完整集成文档](完整集成文档.md) - 系统架构和API文档
2. [项目最终总结](项目最终总结.md) - 项目完成情况

### 演示者
1. [演示步骤](演示步骤.md) - 演示指南
2. API文档: `http://localhost:8000/docs`

## 🎨 界面展示

### AI规划页面 (ai-planner-page.html)
- 标签页设计
- 实时API调用
- 加载动画
- 错误处理
- 响应式布局

### 原完整系统 (health-cube.html)
- 用户登录注册
- 数据追踪
- 食谱推荐
- 运动视频
- AI饮食记录

## 📡 API 接口

### 1. AI饮食计划
```
POST /api/ai/meal-plan
```

### 2. AI运动计划
```
POST /api/ai/workout-plan
```

### 3. AI食物识别
```
POST /api/ai/food-calorie
```

### 4. 身体数据管理
```
POST   /api/user/body-data
GET    /api/user/body-data/history
DELETE /api/user/body-data/{id}
```

详细API文档: `http://localhost:8000/docs`

## 💻 使用示例

### 生成饮食计划
```javascript
const response = await fetch('http://localhost:8000/api/ai/meal-plan', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        profile: { gender: 'male', age: 25, height: 170, weight: 65 },
        preferences: { goal: 'lose', calories_budget: 1800 }
    })
});
const data = await response.json();
```

### 识别食物热量
```javascript
const response = await fetch('http://localhost:8000/api/ai/food-calorie', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: '一份鸡胸肉沙拉，大概 200g' })
});
const data = await response.json();
```

## 🔍 故障排除

### 启动失败？
```bash
# 检查端口占用
netstat -ano | findstr :8000
```

### API调用失败？
- 检查 `.env` 中的API密钥
- 确认网络连接正常
- 查看后端日志

### 页面无法访问？
- 确认后端服务已启动
- 检查浏览器控制台
- 验证URL正确

## 🎯 项目亮点

1. **完整的系统集成** - 所有模块无缝协作
2. **智能的AI功能** - 基于大模型的个性化服务
3. **友好的用户界面** - 简洁美观的设计
4. **详细的文档** - 完整的使用和开发指南
5. **可扩展的架构** - 易于添加新功能

## 📊 项目统计

- **代码行数**: 5000+
- **API端点**: 6个
- **功能模块**: 4个
- **文档文件**: 10+个

## 🚧 未来规划

### 短期
- [ ] 图片识别功能
- [ ] 数据可视化
- [ ] 导出报告

### 中期
- [ ] 用户认证
- [ ] 云端同步
- [ ] 移动端适配

### 长期
- [ ] AI语音助手
- [ ] 设备集成
- [ ] 多语言支持

## 📄 许可证

MIT License

## 👥 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 技术支持

- **API文档**: `http://localhost:8000/docs`
- **完整文档**: 查看项目中的 `.md` 文件
- **问题反馈**: GitHub Issues

---

**项目版本**: v2.0.0  
**完成时间**: 2024-11-20  
**状态**: ✅ 完整集成完成

**享受健康生活，从智能规划开始！** 🥗💪🏃‍♂️🤖
