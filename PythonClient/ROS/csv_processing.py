from typing import List
import csv


def csv_read(file_path) -> list:
  rows =[]
  with open(file_path, newline='') as csvfile:

    # 讀取 CSV 檔案內容
    rows = list(csv.reader(csvfile))

  return rows

def csv_write(wirter_content, data_path) -> None:
  file_path = data_path + 'point_cloud_new.csv'
  with open(file_path, 'w', newline='') as csvfile:
    # 建立 CSV 檔寫入器
    writer = csv.writer(csvfile)

    # 寫入一列資料
    for data in wirter_content:
      writer.writerow(data[4:])

def main():
  data_path = "/home/aiotlab/Documents/Unreal-data/2020-11-08-17-01-42/"
  file_name = 'pointcloud.csv'
  file_path = data_path + file_name
  csv_rows = csv_read(file_path)
  csv_write(csv_rows, data_path)

if __name__ == "__main__":
    main()
