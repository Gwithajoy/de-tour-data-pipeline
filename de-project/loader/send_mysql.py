import os
import pandas as pd
from sqlalchemy import create_engine

def to_mysql(base_path: str, table_name: str, user: str, pw: str, host: str, db: str):
    """CSV 파일을 MySQL에 적재"""
    engine = create_engine(f"mysql+pymysql://{user}:{pw}@{host}/{db}")
    csv_dir = os.path.join(base_path, 'csv')
    for fname in os.listdir(csv_dir):
        if fname.endswith(".csv") and table_name in fname:
            df = pd.read_csv(os.path.join(csv_dir, fname))
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            print(f"Uploaded {fname} → {table_name}")
