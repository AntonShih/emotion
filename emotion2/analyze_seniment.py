from langchain_openai import ChatOpenAI
from dotenv import dotenv_values
import json

# 加載環境變量
config = dotenv_values("./.env")

# 初始化 OpenAI 模型
llm = ChatOpenAI(
    model="gpt-3.5-turbo",  # 可改為其他模型
    openai_api_key=config.get("chat_gpt_key")
)

# 定義情緒分析函數
def analyze_sentiment_with_score(review, category):
    """
    分析餐廳或景點評論的情緒。
    :param review: 字符串格式的餐廳或景點評論
    :param place_id: 餐廳或景點名稱或 ID
    :param data_type: "餐廳" 或 "景點"
    :return: 字典格式的分數和解釋
    """
    if category == "restaurant":
        prompt = f"""
        我希望你幫我分析以下餐廳評論的情緒，並以 1.00-10.00 分制進行評分：
        - 1.00 表示非常負面
        - 10.00 表示非常正面
        - 5.00 表示中性

        請依照以下規範完成：
        1. 分別評分「環境」、「食物」、「服務」三個面向，並給出精確的浮點數分數。
        2. 根據評論內容選擇停留時間（30, 60, 90, 120, 150 分鐘擇一）。
        3. 提供總體評價分數及簡要解釋。

        範例解釋：
        - "環境" 可根據座位寬敞程度、清潔度、噪音等評分。
        - "食物" 可根據味道、創意、分量等評分。
        - "服務" 可根據服務態度、速度等評分。
        - "解釋" 應簡要描述以上分數的理由（如：環境舒適，服務稍慢）。

        請務必返回以下 JSON 格式，並**只返回 JSON 結果**：
        {{
            "環境": [1.00-10.00 的分數],
            "食物": [1.00-10.00 的分數],
            "服務": [1.00-10.00 的分數],
            "停留時間": [30, 60, 90, 120, 150 擇一的分鐘數],
            "總體評價": [1.00-10.00 的分數],
            "解釋": "[簡要描述評分理由]"
        }}
        評論：{review}
        """

    elif category == "attraction":
        prompt = f"""
        我希望你幫我分析以下景點評論的情緒，並以 1.00-10.00 分制進行評分：
        - 1.00 表示非常負面
        - 10.00 表示非常正面
        - 5.00 表示中性

        請根據評論內容選擇以下數值，並**僅返回以下格式的 JSON**：
        - "停留時間" 必須是 30, 60, 90, 120, 150 中的一個（分鐘數）
        - "總體評價" 是 1.00 到 10.00 的浮點數
        - "解釋" 簡要描述為什麼給出該分數

        範例輸出：
        {{
            "停留時間": 90,
            "總體評價": 8.5,
            "解釋": "景點非常漂亮，但人較多稍有擁擠。"
        }}

        評論：{review}
        """

    else:
        return {"error": "Invalid review type"}

    # 使用 LLM 模型進行分析
    response = llm.invoke(prompt)
    analysis = response.content
    # .strip()  # 獲取模型的返回內容
    # analysis = analysis.replace("\n", " ")  # 去除所有換行符號

    try:
        # 將返回的字串轉換為 JSON 格式
        result = json.loads(analysis)
        return result
    except json.JSONDecodeError:
        # 如果解析失敗，返回原始字串和錯誤信息
        return {
            "error": "Failed to parse JSON",
            "raw_response": analysis
        }


if __name__ == "__main__":

    test_reviews = [
        {
            "review": "這家餐廳的裝潢非常現代化，座位間隔寬敞，讓人感到舒適。食物口味一流，尤其是招牌牛排，非常嫩滑。服務員態度熱情，但上菜稍有延遲。",
            "place_id": "restaurant_001",
            "review_type": "restaurant",
        },
        {
            "review": "這個景點非常漂亮，景色迷人，特別適合拍照。就是人有點多，感覺有些擁擠。",
            "place_id": "attraction_001",
            "review_type": "attraction",
        },
        {
            "review": "食物很一般，價格有點高，環境也不算特別好。服務態度尚可，但整體體驗不值這個價格。",
            "place_id": "restaurant_002",
            "review_type": "restaurant",
        },
        {
            "review": "這個地方適合短時間停留，風景不錯，但缺乏維護。門票價格倒是挺便宜的。",
            "place_id": "attraction_002",
            "review_type": "attraction",
        }
    ]

    for test_case in test_reviews:
        review = test_case["review"]
        place_id = test_case["place_id"]
        review_type = test_case["review_type"]

        # 調用分析函式
        print(f"正在分析 PlaceID: {place_id}, 類型: {review_type}")
        result = analyze_sentiment_with_score(review, review_type)

        # 顯示結果
        print("分析結果:")
        print(result)
        print("-" * 50)
