import os
import csv

def record_filenames_to_csv_without_txt_extension(folder_path, output_csv):
    """
    將資料夾中的所有檔案名稱記錄到 CSV 文件，並去掉 .txt 副檔名
    :param folder_path: 要遍歷的資料夾路徑
    :param output_csv: 輸出 CSV 文件的路徑
    """
    try:
        # 確保資料夾存在
        if not os.path.exists(folder_path):
            print(f"資料夾不存在: {folder_path}")
            return

        # 獲取資料夾中的所有檔案名稱
        file_names = os.listdir(folder_path)

        # 打開 CSV 文件並寫入檔案名稱
        with open(output_csv, mode='w', encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["File Name"])  # 寫入 CSV 標題
            for name in file_names:
                # 去掉 .txt 副檔名
                if name.endswith(".txt"):
                    name = os.path.splitext(name)[0]
                writer.writerow([name])  # 寫入每個檔案名稱

        print(f"檔案名稱已成功記錄到 CSV 文件：{output_csv}")

    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    # 設定資料夾路徑和輸出 CSV 文件
    folder_path = "./測試"  # 替換為您的資料夾路徑
    output_csv = "全部id.csv"  # 設定輸出的 CSV 文件名

    # 執行函數
    record_filenames_to_csv_without_txt_extension(folder_path, output_csv)
