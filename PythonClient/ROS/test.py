import csv

# 開啟 CSV 檔案
with open('/home/aiotlab/Documents/FCU-data/test.csv', newline='') as csvfile:

  # 讀取 CSV 檔案內容
  rows = csv.reader(csvfile)

  for row in rows:
      print(row)