"""
完整系统测试脚本
测试所有API端点的功能
"""
import requests
import json

API_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_meal_plan():
    """测试AI饮食计划生成"""
    print_section("测试 AI 饮食计划生成")
    
    data = {
        "profile": {
            "gender": "male",
            "age": 25,
            "height": 170.0,
            "weight": 65.0
        },
        "preferences": {
            "goal": "lose",
            "calories_budget": 1800,
            "diet_type": "none",
            "restrictions": [],
            "tastes": []
        }
    }
    
    try:
        response = requests.post(f"{API_URL}/api/ai/meal-plan", json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✓ 饮食计划生成成功")
            print(f"  每日热量目标: {result['daily_calorie_target']} kcal")
            print(f"  目标: {result['goal']}")
            print(f"  餐次数量: {len(result['meals'])}")
            for meal in result['meals']:
                print(f"  - {meal['meal_type']}: {meal['name']} ({meal['calories']} kcal)")
        else:
            print(f"✗ 请求失败: HTTP {response.status_code}")
    except Exception as e:
        print(f"✗ 错误: {e}")

def test_workout_plan():
    """测试AI运动计划生成"""
    print_section("测试 AI 运动计划生成")
    
    data = {
        "profile": {
            "gender": "male",
            "age": 25,
            "height": 170.0,
            "weight": 65.0
        },
        "preferences": {
            "goal": "lose",
            "available_minutes": 60,
            "frequency_per_week": 3,
            "equipment": [],
            "limitations": []
        }
    }
    
    try:
        response = requests.post(f"{API_URL}/api/ai/workout-plan", json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✓ 运动计划生成成功")
            print(f"  总时长: {result['total_duration']} 分钟")
            print(f"  目标: {result['goal']}")
            print(f"  训练环节: {len(result['sessions'])}")
            for session in result['sessions']:
                print(f"  - {session['name']}: {session['duration_minutes']}分钟 ({session['intensity']})")
        else:
            print(f"✗ 请求失败: HTTP {response.status_code}")
    except Exception as e:
        print(f"✗ 错误: {e}")

def test_food_calorie():
    """测试AI食物热量识别"""
    print_section("测试 AI 食物热量识别")
    
    test_cases = [
        "一份鸡胸肉沙拉，大概 200g",
        "一碗牛肉面",
        "一个苹果"
    ]
    
    for query in test_cases:
        print(f"\n测试: {query}")
        try:
            response = requests.post(
                f"{API_URL}/api/ai/food-calorie",
                json={"query": query},
                timeout=30
            )
            if response.status_code == 200:
                result = response.json()
                print(f"✓ 识别成功")
                print(f"  食物: {result['name']}")
                print(f"  热量: {result['calories']} kcal")
                print(f"  健康评分: {'★' * result['health_score']}{'☆' * (5 - result['health_score'])}")
                print(f"  建议: {result['advice']}")
            else:
                print(f"✗ 请求失败: HTTP {response.status_code}")
        except Exception as e:
            print(f"✗ 错误: {e}")

def test_body_data():
    """测试身体数据管理"""
    print_section("测试身体数据管理")
    
    # 保存数据
    print("\n1. 保存身体数据")
    data = {
        "weight": 65.5,
        "height": 170.0,
        "gender": "male",
        "age": 25
    }
    
    try:
        response = requests.post(f"{API_URL}/api/user/body-data", json=data)
        if response.status_code == 200:
            result = response.json()
            print("✓ 保存成功")
            print(f"  ID: {result['id']}")
            print(f"  日期: {result['date']} {result['time']}")
            print(f"  体重: {result['weight']} kg")
            print(f"  BMI: {result['bmi']}")
            record_id = result['id']
        else:
            print(f"✗ 保存失败: HTTP {response.status_code}")
            return
    except Exception as e:
        print(f"✗ 错误: {e}")
        return
    
    # 获取历史记录
    print("\n2. 获取历史记录")
    try:
        response = requests.get(f"{API_URL}/api/user/body-data/history")
        if response.status_code == 200:
            result = response.json()
            print(f"✓ 获取成功")
            print(f"  记录数量: {len(result['records'])}")
            for record in result['records'][-3:]:  # 显示最近3条
                print(f"  - {record['date']}: {record['weight']} kg (BMI: {record['bmi']})")
        else:
            print(f"✗ 获取失败: HTTP {response.status_code}")
    except Exception as e:
        print(f"✗ 错误: {e}")

def test_api_docs():
    """测试API文档访问"""
    print_section("测试 API 文档")
    
    try:
        response = requests.get(f"{API_URL}/docs")
        if response.status_code == 200:
            print("✓ API文档可访问")
            print(f"  URL: {API_URL}/docs")
        else:
            print(f"✗ 访问失败: HTTP {response.status_code}")
    except Exception as e:
        print(f"✗ 错误: {e}")

def main():
    print("\n" + "=" * 60)
    print("  健康魔方 - 完整系统测试")
    print("=" * 60)
    print("\n确保后端服务已启动: python app.py")
    print("API地址:", API_URL)
    
    # 测试连接
    try:
        response = requests.get(f"{API_URL}/docs", timeout=5)
        print("✓ 后端服务运行正常\n")
    except:
        print("✗ 无法连接到后端服务，请先启动服务\n")
        return
    
    # 运行所有测试
    test_meal_plan()
    test_workout_plan()
    test_food_calorie()
    test_body_data()
    test_api_docs()
    
    print("\n" + "=" * 60)
    print("  测试完成")
    print("=" * 60)
    print("\n访问前端页面:")
    print(f"  - 原系统: {API_URL}")
    print(f"  - AI规划页面: {API_URL}/ai-planner-page.html")
    print("\n")

if __name__ == "__main__":
    main()
