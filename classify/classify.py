import pandas as pd

# 定義分類規則
restaurant_types = ["小吃", "餐廳", "咖啡廳", "甜品店/飲料店"]
attraction_types = ["一般商店", "日用品商店", "休閒設施", "伴手禮商店", "室內旅遊景點", "室外旅遊景點",
                    "購物商場", "文化/歷史景點", "自然景點", "一般商店"]

def classify_data_type(new_label_type):
    """
    根據 data_type 分類為 '餐廳' 或 '景點'。
    :param data_type: 原始類型 (string)
    :return: '餐廳', '景點', 或 '未知'
    """
    if new_label_type in restaurant_types:
        return "restaurant"
    elif new_label_type in attraction_types:
        return "attraction"
    else:
        return "未知"  # 如果類型不匹配，標記為未知

# 主程式
if __name__ == "__main__":
    # 讀取原始 CSV 文件
    input_csv = r"C:\Users\TMP214\Desktop\emotion\ETL_df.csv" 
    output_csv = "classified_output.csv"  # 結果輸出文件

    # 讀取 CSV 文件
    df = pd.read_csv(input_csv)

    # 檢查是否包含必要的列
    if not {"place_id", "data_type"}.issubset(df.columns):
        raise ValueError("CSV 文件缺少必要的列：place_id 或 data_type")

    # 根據 data_type 進行分類
    df["category"] = df["new_label_type"].apply(classify_data_type)

    # 將結果保存到同一個 CSV 文件
    df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"分類結果已保存至 {output_csv}")

print(df["data_type"].unique())
