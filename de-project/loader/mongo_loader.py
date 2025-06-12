import pandas as pd
from pymongo import MongoClient

def to_mongo(csv_path: str, mongo_uri: str, db_name: str, collection_name: str):
    """단일 CSV를 MongoDB에 적재"""
    df = pd.read_csv(csv_path, encoding='utf-8')
    client = MongoClient(mongo_uri)
    db = client[db_name]
    coll = db[collection_name]
    records = df.to_dict('records')
    coll.delete_many({})  # 기존 데이터 삭제
    coll.insert_many(records)
    print(f"Inserted {len(records)} docs into {db_name}.{collection_name}")
    client.close()
