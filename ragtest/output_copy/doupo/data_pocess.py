import pandas as pd
from pathlib import Path

# 定义路径
# parquet_path = Path("/root/autodl-tmp/graphrag/ragtest/output/doupo/entities.parquet")
# excel_path = parquet_path.with_suffix(".xlsx")


# parquet_path = Path("/root/autodl-tmp/graphrag/ragtest/output/doupo/relationships.parquet")
# excel_path = parquet_path.with_suffix(".xlsx")


# parquet_path = Path("/root/autodl-tmp/graphrag/ragtest/output/doupo/documents.parquet")
# excel_path = parquet_path.with_suffix(".xlsx")


parquet_path = Path("/root/autodl-tmp/graphrag/ragtest/output/doupo/text_units.parquet")
excel_path = parquet_path.with_suffix(".xlsx")


# 执行转换
pd.read_parquet(parquet_path, engine="pyarrow").to_excel(
    excel_path, 
    index=False, 
    engine="openpyxl"
)

print('finish.')