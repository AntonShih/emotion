import os
import json
import re

# 載入 JSON 文件
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# 儲存清理後的 JSON 文件
def save_text(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)

# 文本清理函數
def clean_text(text):
    text = re.sub(r"\s+", " ", text)  # 去除多餘空白和換行符
    text = re.sub(r"[^\w\s,.!?]", "", text)  # 移除特殊符號
    text = text.strip()  # 去除首尾空白
    return text

# 合併評論並清理函數
def merge_and_clean_reviews(reviews):
    combined_review = ""
    if isinstance(reviews, list):
        for review in reviews:
            if isinstance(review, dict):
                content = review.get("內容", "")
                combined_review += clean_text(content) + " "
    elif isinstance(reviews, dict):
        for key, review in reviews.items():
            if isinstance(review, dict):
                content = review.get("內容", "")
                combined_review += clean_text(content) + " "
    return combined_review.strip()

# 檢查檔案名稱是否重複
def is_file_duplicate(output_folder, file_name):
    """
    檢查輸出資料夾中是否已經存在該檔案名稱
    :param output_folder: 輸出資料夾路徑
    :param file_name: 要檢查的檔案名稱
    :return: True 如果檔案已存在，False 如果檔案不存在
    """
    file_path = os.path.join(output_folder, file_name)
    return os.path.exists(file_path)

# 處理資料夾內所有 JSON 文件，分別儲存每間餐廳的評論
# 並在合併後進行清理
def process_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.json'):
            input_path = os.path.join(input_folder, file_name)
            output_file_name = file_name.replace('.json', '.txt')  # 修改輸出檔案名稱
            output_path = os.path.join(output_folder, output_file_name)

            # 檢查檔案是否已存在
            if is_file_duplicate(output_folder, output_file_name):
                print(f"檔案已存在，跳過：{output_file_name}")
                continue

            try:
                # 讀取文件
                reviews = load_json(input_path)

                # 合併並清理評論
                combined_reviews = merge_and_clean_reviews(reviews)

                # 儲存清理後的評論
                save_text(combined_reviews, output_path)
                print(f"處理完成並儲存：{output_path}")
            except Exception as e:
                print(f"處理 {file_name} 時發生錯誤: {e}")

# 主函數
def main():
    input_folder = r'./總評論2.0'  # 請修改為包含 JSON 文件的資料夾路徑
    output_folder = r'./測試'  # 儲存清理後評論的資料夾路徑

    process_folder(input_folder, output_folder)
    print(f"所有文件處理完成，結果已儲存至資料夾 {output_folder}")

if __name__ == "__main__":
    main()
