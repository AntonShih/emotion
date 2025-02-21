import pandas as pd
import os

def initialize_paths():
    """
    初始化路徑和配置。
    :return: 一個包含所有必要路徑和分類數據的字典
    """
    folder_path = r'./測試'  # 存放評論的資料夾
    category_csv = r'./classified_output.csv'  # 包含 place_id 和分類的 CSV 文件
    output_file = r'./分析結果.csv'  # 分析結果輸出文件
    error_file = r'./error_log.txt'  # 錯誤記錄文件

    # 加載分類數據,category_map 讀取ETL,拿出place_id跟data_type
    category_df = pd.read_csv(category_csv)
    category_map = dict(zip(category_df["place_id"], category_df["category"]))

    # 定義欄位名稱
    fieldnames = ["placeID", "環境", "食物", "服務", "停留時間", "總體評價", "解釋"]
    return {
        "folder_path": folder_path,
        "output_file": output_file,
        "error_file": error_file,
        "category_map": category_map,
        "fieldnames": fieldnames,
    }

if __name__ == "__main__":
    
    try:
        config = initialize_paths()

        # 驗證返回的配置是否包含必要的鍵
        required_keys = ["folder_path", "output_file", "error_file", "category_map", "fieldnames"]
        for key in required_keys:
            if key not in config:
                raise KeyError(f"Missing required configuration key: {key}")

        # 檢查資料夾是否存在
        folder_path = config["folder_path"]
        if not os.path.exists(folder_path):
            print(f"資料夾不存在，創建中: {folder_path}")
            os.makedirs(folder_path)
        else:
            print(f"資料夾已存在: {folder_path}")

        # 檢查分類文件是否存在
        category_csv = './ETL_df.csv'
        if not os.path.exists(category_csv):
            print(f"分類文件不存在: {category_csv}")
        else:
            print(f"分類文件已存在: {category_csv}")
            category_df = pd.read_csv(category_csv)
            print(f"分類文件加載成功，包含 {len(category_df)} 條記錄")

        # 打印其他配置信息
        print(f"分析結果輸出文件: {config['output_file']}")
        print(f"錯誤記錄文件: {config['error_file']}")
        print(f"CSV 欄位名稱: {config['fieldnames']}")
        print(f"已加載分類映射，共 {len(config['category_map'])} 條")

    except Exception as e:
        print(f"初始化失敗: {e}")
