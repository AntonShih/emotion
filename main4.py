import os
from emotion2.analyze_seniment import analyze_sentiment_with_score
from emotion2.duplicate import is_placeid_duplicate
from emotion2.route import initialize_paths
from emotion2.write_to_csv import write_to_csv,log_error


def main():
    # 初始化路徑和配置
    config = initialize_paths()
    # 測試
    folder_path = config["folder_path"]
    # 分析結果csv
    output_file = config["output_file"]
    # error txt
    error_file = config["error_file"]
    # 快速調用category(是餐廳還是景點)
    category_map = config["category_map"]
    # 標頭
    fieldnames = config["fieldnames"]

    # 遍歷 測試 資料夾中的所有文件
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name) # 測試的完整路徑
        place_id = os.path.splitext(file_name)[0] # place_id

        # # 檢查是否重複
        in_output_file = is_placeid_duplicate(output_file, place_id, "csv")
        in_error_file = is_placeid_duplicate(error_file, place_id, "txt")

        # 根據檢查結果打印對應信息
        if in_output_file:
            print(f"PlaceID: {place_id} 已存在於輸出文件 (分析結果)，跳過該檔案。")
            continue
        if in_error_file:
            print(f"PlaceID: {place_id} 已存在於錯誤文件 (error_log)，跳過該檔案。")
            continue


        # # 獲取分類
        category = category_map.get(place_id, "category")

        # 讀取評論文件
        with open(file_path, "r", encoding="utf-8") as file:
            reviews = [line.strip() for line in file if line.strip()]

            # 對每條評論執行情緒分析
            print(f"正在分析 PlaceID: {place_id}, 類型: {category}")
            for review in reviews:
                result = analyze_sentiment_with_score(review[:1000], category)

            # 如果分析失敗，記錄錯誤
                if "error" in result:
                    log_error(place_id, result["error"])
                    continue

            # 將成功結果寫入輸出文件
                result["placeID"] = place_id
                if len(result) < 5 :
                    result["環境"] = 'none'
                    result['食物'] = 'none'
                    result['服務'] = 'none'
                write_to_csv(output_file, result, fieldnames)

    print(f"所有分析結果已儲存至：{output_file}")
    print(f"錯誤記錄保存在：{error_file}")

if __name__ == "__main__":
    main()