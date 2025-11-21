"""
测试 AI 饮食记录与建议功能
"""
import requests
import json

API_URL = "http://localhost:8000/api/ai/food-calorie"

def test_food_calorie_api():
    """测试食物热量分析 API"""
    
    test_cases = [
        "一份鸡胸肉沙拉，大概 200g",
        "一碗牛肉面，加了一个鸡蛋",
        "星巴克大杯拿铁咖啡",
        "麦当劳巨无霸汉堡套餐",
        "一个苹果"
    ]
    
    print("=" * 60)
    print("AI 饮食记录与建议功能测试")
    print("=" * 60)
    
    for i, query in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {query}")
        print("-" * 60)
        
        try:
            response = requests.post(
                API_URL,
                json={"query": query},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ 请求成功")
                print(f"  食物名称: {data['name']}")
                print(f"  热量估算: {data['calories']} kcal")
                print(f"  健康评分: {'★' * data['health_score']}{'☆' * (5 - data['health_score'])} ({data['health_score']}/5)")
                print(f"  数据来源: {'食物热量表' if data['matched_from_table'] else 'AI 智能估算'}")
                print(f"  营养建议: {data['advice']}")
            else:
                print(f"✗ 请求失败: HTTP {response.status_code}")
                print(f"  错误信息: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("✗ 连接失败: 请确保后端服务已启动 (python app.py)")
            break
        except Exception as e:
            print(f"✗ 发生错误: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    test_food_calorie_api()
