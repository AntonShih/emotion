流程 :
1.由於前面資料清洗人員分類貼錯
    所以這邊額外寫一隻classify.py去把etl重新分類

2.前面clean_final.py先將database的json資料做資料清洗
    存取txt到Text_Clean

3.eontion2為所有功能
載入環境變數
    1. 檢查有無重複
    ->有跳過、沒有跑情緒分析
    2.析情緒分 + 分析停留時間
    -> 1.餐廳 2.景點 3. 停留時間['30min'| '60min'| '90min'| '120min'| '150min']  3.錯誤寫入error_log
    3.存入分析結果csv

main():
    placeIDs = wuth open()
    
    for placeID in placeIDs:
        if not a(placeID) :    --> 重複審核
            result = b(評論, type)   --> 情緒分析 
            csv(result, placeID)          --> 存入
        else :
            print(重複)