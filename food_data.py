# food_data.py
"""
食物营养基础数据（给大模型用的“知识表”）

设计目标：
1. 适合 Qwen3 这类大模型做文本匹配：
   - 有中文名 / 英文名 / 常见别名 / 分类
2. 适合 Qwen3-VL 这类视觉大模型：
   - 别名里包含容易从图片联想到的描述（如“炸鸡腿”“可乐”等）
3. 便于直接 json.dumps 之后塞进 prompt 里
   - 字段名全部是英文 + 下划线，避免解析混乱

与其他模块的统一：
- 供 Python 逻辑精细使用：FOOD_ITEMS（详细字段）
- 供 llm_image_calorie 等简单示例用：FOOD_CALORIE_TABLE（{中文名: kcal_per_100g}）
"""

from typing import List, Dict

# 一条食物的字段示例：
# {
#   "id": "rice_plain",
#   "cn_name": "米饭",
#   "en_name": "plain rice",
#   "aliases": ["白米饭", "白饭"],
#   "category": "主食",
#   "unit": "g",                 # 默认按克/毫升
#   "kcal_per_100g": 116,
#   "protein_per_100g": 2.6,     # g / 100g （可选）
#   "fat_per_100g": 0.3,
#   "carb_per_100g": 25.9,
#   "typical_portion_g": 150     # 一般一份有多少克（给模型估份量时参考）
# }

FOOD_ITEMS: List[Dict] = [
    # ===== 主食 =====
    {
        "id": "rice_plain",
        "cn_name": "米饭",
        "en_name": "plain rice",
        "aliases": ["白米饭", "白饭", "一碗米饭"],
        "category": "主食",
        "unit": "g",
        "kcal_per_100g": 116,
        "protein_per_100g": 2.6,
        "fat_per_100g": 0.3,
        "carb_per_100g": 25.9,
        "typical_portion_g": 150,
    },
    {
        "id": "noodles_plain",
        "cn_name": "面条",
        "en_name": "wheat noodles",
        "aliases": ["面条", "拌面", "汤面", "拉面"],
        "category": "主食",
        "unit": "g",
        "kcal_per_100g": 110,
        "protein_per_100g": 3.5,
        "fat_per_100g": 1.0,
        "carb_per_100g": 22.0,
        "typical_portion_g": 200,
    },
    {
        "id": "mantou",
        "cn_name": "馒头",
        "en_name": "steamed bun",
        "aliases": ["白馒头", "大馒头"],
        "category": "主食",
        "unit": "g",
        "kcal_per_100g": 223,
        "protein_per_100g": 7.0,
        "fat_per_100g": 1.5,
        "carb_per_100g": 46.0,
        "typical_portion_g": 80,
    },
    {
        "id": "bread_slice",
        "cn_name": "面包片",
        "en_name": "sliced bread",
        "aliases": ["吐司", "白面包"],
        "category": "主食",
        "unit": "g",
        "kcal_per_100g": 250,
        "protein_per_100g": 8.0,
        "fat_per_100g": 3.5,
        "carb_per_100g": 45.0,
        "typical_portion_g": 30,  # 一片吐司约 25~30g
    },
    {
        "id": "fried_rice",
        "cn_name": "蛋炒饭",
        "en_name": "fried rice with egg",
        "aliases": ["炒饭", "蛋炒饭", "扬州炒饭"],
        "category": "主食",
        "unit": "g",
        "kcal_per_100g": 180,
        "protein_per_100g": 5.0,
        "fat_per_100g": 6.0,
        "carb_per_100g": 26.0,
        "typical_portion_g": 200,
    },
    {
        "id": "dumpling_pork",
        "cn_name": "猪肉饺子",
        "en_name": "pork dumplings",
        "aliases": ["饺子", "水饺", "猪肉水饺"],
        "category": "主食",
        "unit": "g",
        "kcal_per_100g": 210,
        "protein_per_100g": 9.0,
        "fat_per_100g": 9.0,
        "carb_per_100g": 23.0,
        "typical_portion_g": 20,  # 1 只饺子大约 15~25g
    },

    # ===== 肉蛋鱼类 =====
    {
        "id": "chicken_breast",
        "cn_name": "鸡胸肉",
        "en_name": "chicken breast",
        "aliases": ["煎鸡胸肉", "鸡胸肉块", "水煮鸡胸"],
        "category": "肉蛋鱼",
        "unit": "g",
        "kcal_per_100g": 165,
        "protein_per_100g": 31.0,
        "fat_per_100g": 3.6,
        "carb_per_100g": 0.0,
        "typical_portion_g": 120,
    },
    {
        "id": "chicken_wing_fried",
        "cn_name": "炸鸡翅",
        "en_name": "fried chicken wings",
        "aliases": ["炸鸡", "鸡翅", "香辣鸡翅"],
        "category": "肉蛋鱼",
        "unit": "g",
        "kcal_per_100g": 260,
        "protein_per_100g": 18.0,
        "fat_per_100g": 20.0,
        "carb_per_100g": 6.0,
        "typical_portion_g": 40,  # 一只中等鸡翅
    },
    {
        "id": "pork_belly",
        "cn_name": "五花肉",
        "en_name": "pork belly",
        "aliases": ["红烧肉", "五花肉块"],
        "category": "肉蛋鱼",
        "unit": "g",
        "kcal_per_100g": 395,
        "protein_per_100g": 10.0,
        "fat_per_100g": 37.0,
        "carb_per_100g": 0.0,
        "typical_portion_g": 50,
    },
    {
        "id": "beef_lean",
        "cn_name": "牛肉",
        "en_name": "lean beef",
        "aliases": ["瘦牛肉", "牛排"],
        "category": "肉蛋鱼",
        "unit": "g",
        "kcal_per_100g": 250,
        "protein_per_100g": 26.0,
        "fat_per_100g": 15.0,
        "carb_per_100g": 0.0,
        "typical_portion_g": 100,
    },
    {
        "id": "egg_boiled",
        "cn_name": "鸡蛋",
        "en_name": "boiled egg",
        "aliases": ["水煮蛋", "鸡蛋"],
        "category": "肉蛋鱼",
        "unit": "g",
        "kcal_per_100g": 143,
        "protein_per_100g": 13.0,
        "fat_per_100g": 10.0,
        "carb_per_100g": 1.0,
        "typical_portion_g": 50,  # 1 个中等鸡蛋
    },
    {
        "id": "salmon_pan_fried",
        "cn_name": "三文鱼",
        "en_name": "pan-fried salmon",
        "aliases": ["煎三文鱼", "三文鱼排"],
        "category": "肉蛋鱼",
        "unit": "g",
        "kcal_per_100g": 208,
        "protein_per_100g": 20.0,
        "fat_per_100g": 13.0,
        "carb_per_100g": 0.0,
        "typical_portion_g": 100,
    },
    {
        "id": "shrimp_boiled",
        "cn_name": "虾仁",
        "en_name": "boiled shrimp",
        "aliases": ["虾仁", "白灼虾"],
        "category": "肉蛋鱼",
        "unit": "g",
        "kcal_per_100g": 99,
        "protein_per_100g": 24.0,
        "fat_per_100g": 0.3,
        "carb_per_100g": 0.2,
        "typical_portion_g": 80,
    },

    # ===== 蔬菜 =====
    {
        "id": "broccoli_boiled",
        "cn_name": "西兰花",
        "en_name": "broccoli",
        "aliases": ["蒸西兰花", "炒西兰花"],
        "category": "蔬菜",
        "unit": "g",
        "kcal_per_100g": 36,
        "protein_per_100g": 2.8,
        "fat_per_100g": 0.4,
        "carb_per_100g": 7.0,
        "typical_portion_g": 80,
    },
    {
        "id": "tomato_raw",
        "cn_name": "西红柿",
        "en_name": "tomato",
        "aliases": ["番茄", "生西红柿"],
        "category": "蔬菜",
        "unit": "g",
        "kcal_per_100g": 19,
        "protein_per_100g": 0.9,
        "fat_per_100g": 0.2,
        "carb_per_100g": 4.0,
        "typical_portion_g": 120,
    },
    {
        "id": "cucumber_raw",
        "cn_name": "黄瓜",
        "en_name": "cucumber",
        "aliases": ["生黄瓜", "拍黄瓜"],
        "category": "蔬菜",
        "unit": "g",
        "kcal_per_100g": 15,
        "protein_per_100g": 1.0,
        "fat_per_100g": 0.2,
        "carb_per_100g": 3.0,
        "typical_portion_g": 100,
    },
    {
        "id": "potato_boiled",
        "cn_name": "土豆",
        "en_name": "potato",
        "aliases": ["马铃薯", "土豆块"],
        "category": "蔬菜",
        "unit": "g",
        "kcal_per_100g": 80,
        "protein_per_100g": 2.0,
        "fat_per_100g": 0.1,
        "carb_per_100g": 18.0,
        "typical_portion_g": 100,
    },

    # ===== 水果 =====
    {
        "id": "apple_raw",
        "cn_name": "苹果",
        "en_name": "apple",
        "aliases": ["红苹果", "青苹果"],
        "category": "水果",
        "unit": "g",
        "kcal_per_100g": 52,
        "protein_per_100g": 0.3,
        "fat_per_100g": 0.2,
        "carb_per_100g": 14.0,
        "typical_portion_g": 150,
    },
    {
        "id": "banana_raw",
        "cn_name": "香蕉",
        "en_name": "banana",
        "aliases": ["香蕉", "一根香蕉"],
        "category": "水果",
        "unit": "g",
        "kcal_per_100g": 93,
        "protein_per_100g": 1.3,
        "fat_per_100g": 0.3,
        "carb_per_100g": 23.0,
        "typical_portion_g": 100,
    },
    {
        "id": "orange_raw",
        "cn_name": "橙子",
        "en_name": "orange",
        "aliases": ["甜橙", "橙子瓣"],
        "category": "水果",
        "unit": "g",
        "kcal_per_100g": 47,
        "protein_per_100g": 0.9,
        "fat_per_100g": 0.1,
        "carb_per_100g": 12.0,
        "typical_portion_g": 150,
    },

    # ===== 奶制品 =====
    {
        "id": "milk_whole",
        "cn_name": "全脂牛奶",
        "en_name": "whole milk",
        "aliases": ["牛奶", "一杯牛奶"],
        "category": "奶制品",
        "unit": "ml",
        "kcal_per_100g": 64,        # 近似：64 kcal / 100ml
        "protein_per_100g": 3.2,
        "fat_per_100g": 3.6,
        "carb_per_100g": 4.8,
        "typical_portion_g": 250,   # 当作 250ml ≈ 250g
    },
    {
        "id": "yogurt_plain",
        "cn_name": "酸奶",
        "en_name": "plain yogurt",
        "aliases": ["原味酸奶", "常温酸奶"],
        "category": "奶制品",
        "unit": "g",
        "kcal_per_100g": 70,
        "protein_per_100g": 3.0,
        "fat_per_100g": 3.0,
        "carb_per_100g": 8.0,
        "typical_portion_g": 200,
    },

    # ===== 饮料 & 甜品 =====
    {
        "id": "coke",
        "cn_name": "可乐",
        "en_name": "cola",
        "aliases": ["可乐", "零度可乐", "汽水"],
        "category": "饮料",
        "unit": "ml",
        "kcal_per_100g": 42,       # 正常糖可乐
        "protein_per_100g": 0.0,
        "fat_per_100g": 0.0,
        "carb_per_100g": 10.6,
        "typical_portion_g": 330,  # 一听
    },
    {
        "id": "milk_tea_sweet",
        "cn_name": "奶茶",
        "en_name": "sweet milk tea",
        "aliases": ["珍珠奶茶", "奶茶", "全糖奶茶"],
        "category": "饮料",
        "unit": "ml",
        "kcal_per_100g": 80,
        "protein_per_100g": 1.2,
        "fat_per_100g": 2.0,
        "carb_per_100g": 14.0,
        "typical_portion_g": 500,
    },
    {
        "id": "orange_juice",
        "cn_name": "橙汁饮料",
        "en_name": "orange juice drink",
        "aliases": ["橙汁", "果汁饮料"],
        "category": "饮料",
        "unit": "ml",
        "kcal_per_100g": 45,
        "protein_per_100g": 0.5,
        "fat_per_100g": 0.0,
        "carb_per_100g": 11.0,
        "typical_portion_g": 250,
    },
    {
        "id": "cake_cream",
        "cn_name": "奶油蛋糕",
        "en_name": "cream cake",
        "aliases": ["蛋糕", "生日蛋糕", "奶油蛋糕"],
        "category": "甜点",
        "unit": "g",
        "kcal_per_100g": 330,
        "protein_per_100g": 6.0,
        "fat_per_100g": 20.0,
        "carb_per_100g": 32.0,
        "typical_portion_g": 80,
    },
    {
        "id": "cookie_biscuit",
        "cn_name": "曲奇饼干",
        "en_name": "cookies",
        "aliases": ["饼干", "曲奇", "小饼干"],
        "category": "甜点",
        "unit": "g",
        "kcal_per_100g": 480,
        "protein_per_100g": 6.0,
        "fat_per_100g": 23.0,
        "carb_per_100g": 64.0,
        "typical_portion_g": 20,   # 一小块
    },
    {
        "id": "ice_cream",
        "cn_name": "冰淇淋",
        "en_name": "ice cream",
        "aliases": ["冰激凌", "雪糕"],
        "category": "甜点",
        "unit": "g",
        "kcal_per_100g": 200,
        "protein_per_100g": 3.5,
        "fat_per_100g": 11.0,
        "carb_per_100g": 23.0,
        "typical_portion_g": 80,
    },
]


# ========= 与其他模块统一用的简单结构 =========
# llm_image_calorie.py 里会直接:
#   from food_data import FOOD_CALORIE_TABLE
#   table_text = "\\n".join(f"- {name}: {kcal} kcal" for name, kcal in FOOD_CALORIE_TABLE.items())
#
# 这里给出一个「中文名 -> 每 100g 热量」的简化映射。

FOOD_CALORIE_TABLE: Dict[str, int] = {
    item["cn_name"]: int(item["kcal_per_100g"]) for item in FOOD_ITEMS
}


def get_food_items() -> List[Dict]:
    """给 Python 逻辑使用：返回完整列表。"""
    return FOOD_ITEMS


def get_food_table_for_llm() -> List[Dict]:
    """
    给大模型使用：目前直接返回 FOOD_ITEMS，
    以后如果需要精简字段（例如只保留 cn_name、aliases、kcal_per_100g），
    可以在这里做一层转换。
    """
    return FOOD_ITEMS
