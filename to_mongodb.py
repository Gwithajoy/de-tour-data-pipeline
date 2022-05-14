from pymongo import MongoClient
import traceback
import pandas as pd

def main():
    host='ec2-52-79-243-3.ap-northeast-2.compute.amazonaws.com'
    port = 27017
    try: 
        client = MongoClient(
            host=host,
            port=port 
        )
        db = client['naver']
        collection = db['코엑스']
        df = pd.read_csv('/Users/glebang/Desktop/team4/csv/코엑스.csv', encoding='utf-8')
        data = df.to_dict('records')
        insertion = collection.insert_many(data)
        print(collection.find_one())
    except Exception as e:
        print(traceback.format_exc())
     
    finally:
        client.close()
        print('Mongodb closed.')
        
if __name__ == '__main__':
    main()