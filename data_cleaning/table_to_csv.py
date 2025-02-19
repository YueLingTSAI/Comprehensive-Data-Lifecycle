import mysql.connector
import csv

# 連接資料庫
conn = mysql.connector.connect(
    host="labdb.coded2.fun", user="sophia", password="1234dv107", database="SOPHIA"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM dcard")  # 查詢資料(改成你的TABLE)

# 打開 CSV 檔案並寫入資料(自訂csv檔名)
with open("dcard_data.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file, quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow([desc[0] for desc in cursor.description])  # 寫入欄位名
    for row in cursor:
        writer.writerow(row)

# 關閉連線
cursor.close()
conn.close()

print("CSV 匯出完成！")
