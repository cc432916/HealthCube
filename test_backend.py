"""
测试后端服务是否正常运行
"""
import requests

API_URL = "http://localhost:8000"

def test_backend():
    print("=" * 60)
    print("  测试后端服务")
    print("=" * 60)
    
    # 测试根路径
    print("\n1. 测试根路径...")
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        if response.status_code == 200:
            print("✓ 根路径访问成功")
        else:
            print(f"✗ 根路径返回: HTTP {response.status_code}")
    except Exception as e:
        print(f"✗ 无法连接到后端服务")
        print(f"  错误: {e}")
        print("\n请先启动后端服务:")
        print("  python app.py")
        return False
    
    # 测试 API 文档
    print("\n2. 测试 API 文档...")
    try:
        response = requests.get(f"{API_URL}/docs", timeout=5)
        if response.status_code == 200:
            print("✓ API 文档可访问")
            print(f"  URL: {API_URL}/docs")
        else:
            print(f"✗ API 文档返回: HTTP {response.status_code}")
    except Exception as e:
        print(f"✗ API 文档访问失败: {e}")
    
    # 测试食物识别 API
    print("\n3. 测试食物识别 API...")
    try:
        response = requests.post(
            f"{API_URL}/api/ai/food-calorie",
            json={"query": "一个苹果"},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            print("✓ 食物识别 API 正常")
            print(f"  食物: {data['name']}")
            print(f"  热量: {data['calories']} kcal")
        else:
            print(f"✗ 食物识别 API 返回: HTTP {response.status_code}")
            print(f"  响应: {response.text}")
    except Exception as e:
        print(f"✗ 食物识别 API 失败: {e}")
    
    print("\n" + "=" * 60)
    print("  测试完成")
    print("=" * 60)
    print("\n如果所有测试都通过，可以访问:")
    print(f"  {API_URL}")
    print("\n")
    return True

if __name__ == "__main__":
    test_backend()
