import csv
import os

def is_placeid_duplicate(file_path, place_id, file_type):
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

# if __name__ == "__main__":

# # 測試文件路徑
#     csv_file = r"./test_places.csv"
#     txt_file = r"./test_places.txt"

#     # # 測試數據
#     # test_data = [
#     #     {"place_id": "place_001", "name": "Place A", "type": "restaurant"},
#     #     {"place_id": "place_002", "name": "Place B", "type": "attraction"},
#     #     {"place_id": "place_003", "name": "Place C", "type": "restaurant"},
#     # ]


#     # 測試 PlaceID 是否重複
#     test_place_ids = ["place_001", "place_004"]

#     for place_id in test_place_ids:
#         print(f"Testing PlaceID: {place_id} in CSV file...")
#         is_duplicate = is_placeid_duplicate(csv_file, place_id, "csv")
#         print(f"Is duplicate in CSV? {is_duplicate}")

#         print(f"Testing PlaceID: {place_id} in TXT file...")
#         is_duplicate = is_placeid_duplicate(txt_file, place_id, "txt")
#         print(f"Is duplicate in TXT? {is_duplicate}")

#     # 清理測試文件
#     # os.remove(csv_file)
#     # os.remove(txt_file)