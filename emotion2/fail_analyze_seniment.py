# from langchain_openai import ChatOpenAI
# from dotenv import dotenv_values
# # 加載環境變量
# config = dotenv_values("./.env")

# # 初始化 OpenAI 模型
# llm = ChatOpenAI(
#     model="gpt-3.5-turbo",  # 可改為其他模型
#     openai_api_key=config.get("chat_gpt_key")
# )


# # 定義情緒分析函數
# def analyze_sentiment_with_score(review, place_id, review_type):
#     """
#     分析餐廳或景點評論的情緒。
#     :param review: 字符串格式的餐廳或景點評論
#     :param place_id: 餐廳或景點名稱或 ID
#     :param review_type: "餐廳" 或 "景點"
#     :return: 字典格式的分數和解釋
#     """
#     if review_type == "餐廳":
#         prompt = f"""
#         我希望你幫我分析以下餐廳評論的情緒，並以 1.00-10.00 分制進行評分：
#         1.00 表示非常負面，10.00 表示非常正面，5.00 表示中性。
#         請依照環境、食物、服務三個面向給出細膩的浮點數分數，並依照評論內容選擇一個['30'| '60'| '90'| '120'| '150']分的停留時間
#         你只需要填入<>內的內容：
        
#         環境: <分數> 分
#         食物: <分數> 分
#         服務: <分數> 分
#         總體評價: <分數> 分
#         解釋: <簡要解釋為什麼給出該分數及該餐廳的重點評價>
#         停留時間:<['30'| '60'| '90'| '120'| '150']>分
        
#         評論：{review}
#         """
#     elif review_type == "景點":
#         prompt = f"""
#         我希望你幫我分析以下景點評論的情緒，並以 1.00-10.00 分制進行評分：
#     - 1.00 表示非常負面
#     - 10.00 表示非常正面
#     - 5.00 表示中性

#     請根據評論內容選擇以下數值，並**僅返回以下格式的 JSON**：
#     - "停留時間" 必須是 30, 60, 90, 120, 150 中的一個（分鐘數）
#     - "總體評價" 是 1.00 到 10.00 的浮點數
#     - "解釋" 簡要描述為什麼給出該分數

#     範例輸出：
#     {{
#         "停留時間": 90,
#         "總體評價": 8.5,
#         "解釋": "景點非常漂亮，但人較多稍有擁擠。"
#     }}

#     評論：{review}
#     """
#     else:
#         return {"error": "Invalid review type"}
#     # 不是餐廳也不是景點
    
#     try:
#             response = llm.invoke(prompt)
#             analysis = response.content.strip()  # 獲取模型的返回內容
#             analysis = analysis.replace("\n", " ")  # 去除所有換行符號

            
#             if review_type == "餐廳":
#                 result = {
#                     "placeID": place_id,
#                     "類型": review_type,
#                     "環境": extract_value(analysis, "環境"),
#                     "食物": extract_value(analysis, "食物"),
#                     "服務": extract_value(analysis, "服務"),
#                     "停留時間": extract_value(analysis, "停留時間"),
#                     "總體評價": extract_value(analysis, "總體評價"),
#                     "解釋": extract_value(analysis, "解釋"),
#                 }
#             elif review_type == "景點":
#                 result = {
#                     "placeID": place_id,
#                     "類型": review_type,
#                     "環境": "N/A",  # 景點評論不需要此項
#                     "食物": "N/A",  # 景點評論不需要此項
#                     "服務": "N/A",  # 景點評論不需要此項
#                     "停留時間": extract_value(analysis, "停留時間"),
#                     "總體評價": extract_value(analysis, "總體評價"),
#                     "解釋": extract_value(analysis, "解釋"),
#                 }
#             return result
    
#     except Exception as e:
#             return {"error": f"An error occurred: {e}"}
#     # 如果发生了文件未找到错误，e 可能是 FileNotFoundError: [Errno 2] No such file or directory.
    

# # # 提取結果的函數
# def extract_value(text, key):
#     """
#     從模型生成的文本中提取指定鍵的值
#     :param text: 模型返回的分析結果
#     :param key: 要提取的鍵（如 環境、食物）
#     :return: 鍵對應的值
#     """
#     try:
#         start = text.find(f"{key}: ") + len(f"{key}: ")
#         end = text.find(" 分", start) if key != "解釋" else len(text)
#         return text[start:end].strip()
#     except:
#         return "N/A"  # 若解析失敗，返回 "N/A"
    
# if __name__ == "__main__":

#      test_reviews = [
#         {
#             "review": "這家餐廳的裝潢非常現代化，座位間隔寬敞，讓人感到舒適。食物口味一流，尤其是招牌牛排，非常嫩滑。服務員態度熱情，但上菜稍有延遲。",
#             "place_id": "restaurant_001",
#             "review_type": "餐廳",
#         },
#         {
#             "review": "這個景點非常漂亮，景色迷人，特別適合拍照。就是人有點多，感覺有些擁擠。",
#             "place_id": "attraction_001",
#             "review_type": "景點",
#         },
#         {
#             "review": "食物很一般，價格有點高，環境也不算特別好。服務態度尚可，但整體體驗不值這個價格。",
#             "place_id": "restaurant_002",
#             "review_type": "餐廳",
#         },
#         {
#             "review": "這個地方適合短時間停留，風景不錯，但缺乏維護。門票價格倒是挺便宜的。",
#             "place_id": "attraction_002",
#             "review_type": "景點",
#         }
#     ]
        
#      for test_case in test_reviews:
#         review = test_case["review"]
#         place_id = test_case["place_id"]
#         review_type = test_case["review_type"]

#         # 調用分析函式
#         print(f"正在分析 PlaceID: {place_id}, 類型: {review_type}")
#         result = analyze_sentiment_with_score(review, place_id, review_type)

#         # 顯示結果
#         print("分析結果:")
#         print(result)
#         print("-" * 50)