
import csv
import os

def write_to_csv(file_path, result, fieldnames):
    """
    將分析結果寫入 CSV 文件。
    :param file_path: 要寫入的 CSV 文件路徑
    :param result: 一個包含結果的字典
    :param fieldnames: CSV 文件的欄位名稱列表
    """
    # 檢查文件是否存在，若不存在則初始化並寫入標題行
    file_exists = os.path.exists(file_path)
    with open(file_path, mode="a", encoding="utf-8", newline="") as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            csv_writer.writeheader()  # 如果文件不存在，先寫入標題行
        csv_writer.writerow(result)  # 寫入單行結果

def log_error(place_id, message):
    """
    記錄錯誤到錯誤日誌文件。
    :param place_id: 錯誤相關的 PlaceID
    :param message: 錯誤信息
    """
    with open("error_log.txt", "a", encoding="utf-8") as log:
        log.write(f"{place_id},{message}\n")
        # 路徑不要寫死，才能測試

# if __name__ == "__main__":
#         # 測試數據
#     test_results = [
#         {
#             "placeID": "place_001",
#             "環境": 8.5,
#             "食物": 9.0,
#             "服務": 7.5,
#             "停留時間": 90,
#             "總體評價": 8.7,
#             "解釋": "環境舒適，食物美味，服務稍慢。"
#         },
#         {
#             "placeID": "place_002",
#             "環境": 6.0,
#             "食物": 5.5,
#             "服務": 7.0,
#             "停留時間": 60,
#             "總體評價": 6.2,
#             "解釋": "環境一般，食物普通，服務尚可。"
#         }
#     ]

#     # 測試文件路徑
#     output_file = r"./test_places.csv"
#     txt_file = r"./test_places.txt"
#     fieldnames = ["placeID", "環境", "食物", "服務", "停留時間", "總體評價", "解釋"]

#     # 測試寫入結果
#     for result in test_results:
#         write_to_csv(output_file, result, fieldnames)
#         print(f"已寫入結果：{result['placeID']}")

# def write_test_data_to_txt(file_path, test_results):
#     """
#     將測試數據寫入指定的 TXT 文件。
#     :param file_path: 要寫入的 TXT 文件路徑
#     :param test_results: 測試數據列表
#     """
#     with open(file_path, "w", encoding="utf-8") as txt_file:
#         for result in test_results:
#             txt_file.write(f"{result}\n")

#     # 測試寫入結果到 TXT
# write_test_data_to_txt(txt_file, test_results)
# print(f"已寫入所有測試數據到 TXT 文件：{txt_file}")

#     # 測試錯誤日誌
# log_error("place_003", "錯誤信息")
# print("已記錄錯誤：place_003 到 error_log.txt")