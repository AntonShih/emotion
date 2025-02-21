import os
import pandas as pd
from langchain_openai import ChatOpenAI
from dotenv import dotenv_values
import csv  # 匯入 csv 模組，用於寫入 CSV 文件

# 加載環境變量
config = dotenv_values("./.env")

# 初始化 OpenAI 模型
llm = ChatOpenAI(
    model="gpt-3.5-turbo",  # 可改為其他模型
    openai_api_key=config.get("chat_gpt_key")
)

# 定義情緒分析函數
def analyze_sentiment_with_score(review, place_id, review_type):
    """
    分析餐廳或景點評論的情緒。
    :param review: 字符串格式的餐廳或景點評論
    :param place_id: 餐廳或景點名稱或 ID
    :param review_type: "餐廳" 或 "景點"
    :return: 字典格式的分數和解釋
    """
    if review_type == "餐廳":
        prompt = f"""
        我希望你幫我分析以下餐廳評論的情緒，並以 1.00-10.00 分制進行評分：
        1.00 表示非常負面，10.00 表示非常正面，5.00 表示中性。
        請依照環境、食物、服務三個面向給出細膩的浮點數分數，你只需要填入<>內的內容：
        
        環境: <分數> 分
        食物: <分數> 分
        服務: <分數> 分
        總體評價: <分數> 分
        解釋: <簡要解釋為什麼給出該分數及該餐廳的重點評價>
        
        評論：{review}
        """
    elif review_type == "景點":
        prompt = f"""
        我希望你幫我分析以下景點評論的情緒，並以 1.00-10.00 分制進行的評分：
        1.00 表示非常負面，10.00 表示非常正面，5.00 表示中性。
        你只需要填入<>內的內容：
        
        總體評價: <分數> 分
        解釋: <簡要解釋為什麼給出該分數>
        
        評論：{review}
        """
    else:
        return {"error": "Invalid review type"}
    # 不是餐廳也不是景點
    
    try:
            response = llm.invoke(prompt)
            analysis = response.content.strip()  # 獲取模型的返回內容
            analysis = analysis.replace("\n", " ")  # 去除所有換行符號

            
            if review_type == "餐廳":
                result = {
                    "placeID": place_id,
                    "類型": review_type,
                    "環境": extract_value(analysis, "環境"),
                    "食物": extract_value(analysis, "食物"),
                    "服務": extract_value(analysis, "服務"),
                    "總體評價": extract_value(analysis, "總體評價"),
                    "解釋": extract_value(analysis, "解釋"),
                }
            elif review_type == "景點":
                result = {
                    "placeID": place_id,
                    "類型": review_type,
                    "環境": "N/A",  # 景點評論不需要此項
                    "食物": "N/A",  # 景點評論不需要此項
                    "服務": "N/A",  # 景點評論不需要此項
                    "總體評價": extract_value(analysis, "總體評價"),
                    "解釋": extract_value(analysis, "解釋"),
                }
            return result
    
    except Exception as e:
            return {"error": f"An error occurred: {e}"}
    # 如果发生了文件未找到错误，e 可能是 FileNotFoundError: [Errno 2] No such file or directory.
    

# # 提取結果的函數
def extract_value(text, key):
    """
    從模型生成的文本中提取指定鍵的值
    :param text: 模型返回的分析結果
    :param key: 要提取的鍵（如 環境、食物）
    :return: 鍵對應的值
    """
    try:
        start = text.find(f"{key}: ") + len(f"{key}: ")
        end = text.find(" 分", start) if key != "解釋" else len(text)
        return text[start:end].strip()
    except:
        return "N/A"  # 若解析失敗，返回 "N/A"
    
# # 定義檢查是否有重複 placeID 的函數
# def is_placeid_duplicate(output_file, place_id):
#     """
#     檢查輸出的 CSV 文件中是否已經存在相同的 placeID。
#     :param output_file: CSV 文件的路徑
#     :param place_id: 要檢查的 placeID
#     :return: True 如果 placeID 已存在，False 如果不存在
#     """
#     # if not os.path.exists(output_file):
#     #     return False  # 如果檔案不存在，placeID 不可能重複

#     # output_file = csvfile但在with結束後就自動結束
#     with open(output_file, mode="r", encoding="utf-8") as csvfile:
#         csv_reader = csv.DictReader(csvfile)
#         for row in csv_reader:
#             if row["place_id"] == place_id:
#                 return True
#     return False

def is_placeid_duplicate(file_path, place_id, file_type="csv"):
    """
    通用檢查文件中是否已經存在相同的 PlaceID。
    :param file_path: 文件的路徑
    :param place_id: 要檢查的 PlaceID
    :param file_type: 文件類型 ("csv" 或 "txt")
    :return: True 如果 PlaceID 已存在，False 如果不存在
    """

    with open(file_path, mode="r", encoding="utf-8") as file:
        if file_type == "csv":
            csv_reader = csv.DictReader(file)
        elif file_type == "txt":
            csv_reader = csv.DictReader(file)  # 假設 TXT 文件也是逗號分隔
        else:
            raise ValueError("Unsupported file type. Use 'csv' or 'txt'.")
        
        for row in csv_reader:
            if row["place_id"] == place_id:
                return True
    return False


# 主程式
if __name__ == "__main__":
    # 資料夾路徑
    folder_path = r'./測試'  # 替換為您的資料夾路徑
    category_csv = r'./classified_output.csv'  # 包含 place_id 和 category 的 CSV 文件
    output_file = r'./分析結果.csv'  # 分析結果輸出的 CSV 文件
    error_list = r'./error_log.txt'

    # 從 CSV 文件中讀取 place_id 和 category
    # classified_output.csv就是category_csv，將 place_id 和 category 映射為字典，方便快速查詢每個 place_id 的分類
    category_df = pd.read_csv(category_csv)
    category_map = dict(zip(category_df["place_id"], category_df["category"]))

    # 初始化 CSV 文件，寫入標題行（若檔案不存在）
    if not os.path.exists(output_file):
        with open(output_file, mode="w", encoding="utf-8", newline="") as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=["place_id", "類型", "環境", "食物", "服務", "總體評價", "解釋"])
            csv_writer.writeheader()  # 寫入標題行

    # 遍歷測試資料夾內的所有檔案
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):  # 只處理 .txt 檔案
            file_path = os.path.join(folder_path, file_name)  # 完整檔案路徑(在測試檔案中的所有路徑)
            place_id = os.path.splitext(file_name)[0]  # 取檔案名稱作為 placeID

            # # 檢查是否已經存在於輸出文件中
            # if is_placeid_duplicate(output_file, place_id,"csv"): #分析結果跟id
            #     print(f"PlaceID: {place_id} 已存在於輸出文件中，跳過該檔案。") #is_placeid_duplicate回傳true就繼續
            #     continue

            # if is_placeid_duplicate(error_list, place_id,"txt"): #分析結果跟id
            #     print(f"PlaceID: {place_id} 已存在於輸出文件中，跳過該檔案。") #is_placeid_duplicate回傳true就繼續
            #     continue
            # 定義需要檢查的文件和類型
            files_to_check = [
                {"file_path": output_file, "file_type": "csv"},
                {"file_path": error_list, "file_type": "txt"},
            ]

            for file in files_to_check:
                if is_placeid_duplicate(file["file_path"], place_id, file["file_type"]):
                    print(f"PlaceID: {place_id} 已存在於 {file['file_path']} 中，跳過該檔案。")
                    continue  # 如果已找到重複項，跳過後續檢查
            # else:
            #     # 如果沒有任何檔案中有重複，繼續後續處理邏輯
            #     print(f"PlaceID: {place_id} 不存在於任何文件中，進行處理。")


            # 根據 place_id 獲取 category
            review_type = category_map.get(place_id, "未知")

            if review_type == "未知":
                print(f"PlaceID: {place_id} 無法找到對應的分類，跳過該檔案。")
                with open("error_log.txt", "a", encoding="utf-8") as log_file:
                        # log_file.write(f"PlaceID: {place_id}, Error: 無法找到對應分類。\n")
                    log_file.write(f"{place_id},{'無法找到對應分類'}\n")
                continue  # 跳過該條目，不寫入 CSV


            # 讀取測試中評論內容
            with open(file_path, "r", encoding="utf-8") as file:
                text_content = file.read().splitlines()  # 按行分割為列表

            reviews = [line for line in text_content if line.strip()]  # 去除空行

            print(f"分析檔案: {file_name}")#分析測試檔案
            
            for review in reviews:
                # 調用分析函數，獲取分析結果
                result = analyze_sentiment_with_score(review[:5000], place_id, review_type)
                print(result)  # 列印結果

                # # 處理錯誤結果
                # if "error" in result:
                #     # 記錄錯誤到日誌文件
                #     with open("error_log.txt", "a", encoding="utf-8") as log_file:
                #         log_file.write(f"PlaceID: {place_id}, Review: {review[:100]}..., Error: {result['error']}\n")
                #     continue  # 跳過該條目，不寫入 CSV

                 # 處理錯誤結果
                if "error" in result:
                    # 記錄錯誤到日誌文件
                    with open("error_log.txt", "a", encoding="utf-8") as log_file:
                        log_file.write(f"{place_id},{result['error']}\n")
                    continue  # 跳過該條目，不寫入 CSV

                # 將結果寫入 CSV 文件
                with open(output_file, mode="a", encoding="utf-8", newline="") as csvfile:
                    csv_writer = csv.DictWriter(csvfile, fieldnames=["placeID", "類型", "環境", "食物", "服務", "總體評價", "解釋"])
                    csv_writer.writerow(result)

    print(f"所有分析結果已儲存為 CSV 檔案：{output_file}")
