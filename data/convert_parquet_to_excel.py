import pandas as pd 
# pip install openpyxl

parquet_path = "/root/autodl-tmp/graphrag/ragtest/output/doupo/communities.parquet"
excel_path = "/root/autodl-tmp/graphrag/ragtest/output/doupo/communities.xlsx"

try:
    df = pd.read_parquet(parquet_path)
    print("Parquet文件读取成功，数据形状：", df.shape)
except FileNotFoundError:
    print(f"错误：未找到文件 {parquet_path}")
    exit(1)
except Exception as e:
    print(f"读取文件失败：{str(e)}")
    exit(1)

try:
    df.to_excel(excel_path, index=False, engine="openpyxl")
    print(f"Excel文件已成功保存至：{excel_path}")
except Exception as e:
    print(f"保存Excel失败：{str(e)}")
    exit(1)
