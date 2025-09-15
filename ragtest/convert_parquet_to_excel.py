# 安装所需库（首次运行时取消注释）
# !pip install pandas pyarrow openpyxl

import pandas as pd
import os

# 1. 加载 parquet 文件
file_path_parquet = r'C:\Users\lizhong\Documents\codes\graphrag\ragtest\output\doupo\documents.parquet'  # 请确保文件路径正确
# df = pd.read_parquet(file_path_parquet)

# # 2. 查看前几行数据（可选，用于确认内容）
# print("数据预览：")
# print(df.head())

# # 3. 保存为 Excel 文件
# output_excel = r'C:\Users\lizhong\Documents\codes\graphrag\ragtest\output\doupo\documents.xlsx'
# df.to_excel(output_excel, index=False, engine='openpyxl')

# print(f"\n✅ 数据已成功保存为 '{output_excel}'，可用 Excel 打开查看。")


def convert(file):
    df = pd.read_parquet(file)
    print(df.head())

    output_file = file.split(".")[0] + '.xlsx'
    df.to_excel(output_file, index=False, engine="openpyxl") 
    print(f"\n✅ 数据已成功保存为 '{output_file}'，可用 Excel 打开查看。")


if __name__ == "__main__":
    # file = r'C:\Users\lizhong\Documents\codes\graphrag\ragtest\output\doupo\documents.parquet'  # 请确保文件路径正确
    # convert(file)

    file = r'C:\Users\lizhong\Documents\codes\graphrag\ragtest\output\doupo\text_units.parquet'  # 请确保文件路径正确
    convert(file)