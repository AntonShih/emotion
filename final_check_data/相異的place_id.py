import pandas as pd

def compare_place_ids(csv_file1, csv_file2, output_file):
    """
    比較兩個 CSV 檔案中的 place_id 列，找出差異部分並保存到輸出文件
    :param csv_file1: 第一個 CSV 文件路徑
    :param csv_file2: 第二個 CSV 文件路徑
    :param output_file: 輸出差異的 CSV 文件路徑
    """
    try:
        # 讀取兩個 CSV 文件
        df1 = pd.read_csv(csv_file1, dtype={"place_id": str})  # 確保 place_id 為 str
        df2 = pd.read_csv(csv_file2, dtype={"place_id": str})  # 確保 place_id 為 str

        # 確保 place_id 列存在
        if 'place_id' not in df1.columns or 'place_id' not in df2.columns:
            print("CSV 文件中未找到 'place_id' 列")
            return

        # 獲取兩個文件的 place_id 集合（轉為字符串確保一致性）
        place_ids1 = set(df1['place_id'].astype(str))
        place_ids2 = set(df2['place_id'].astype(str))

        # 計算差異
        only_in_file1 = place_ids1 - place_ids2  # 只存在於文件1中的 place_id
        only_in_file2 = place_ids2 - place_ids1  # 只存在於文件2中的 place_id

        # 組織結果為 DataFrame
        result_df = pd.DataFrame(
            {
                "Category": ["only_in_file1"] * len(only_in_file1) + ["only_in_file2"] * len(only_in_file2),
                "Place ID": list(only_in_file1) + list(only_in_file2),
            }
        )

        # 保存結果到輸出文件
        result_df.to_csv(output_file, index=False, encoding="utf-8")
        print(f"差異已成功保存至：{output_file}")

    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    # 設定兩個輸入 CSV 文件路徑和輸出文件路徑
    csv_file1 = r"./全部id.csv"  # 替換為您的第一個 CSV 文件路徑
    csv_file2 = r"./分析結果.csv"  # 替換為您的第二個 CSV 文件路徑
    output_file = r"相異的place_id.csv"  # 設定輸出文件路徑

    # 執行比較函數
    compare_place_ids(csv_file1, csv_file2, output_file)

