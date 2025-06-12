import os
from crawler.navigation_crawler import (
    get_driver, login, goto_metric, build_date_ranges, crawl
)
from processor.sort_and_download import sort_by_location_year_month
from loader.send_mysql import to_mysql
from loader.mongo_loader import to_mongo

# 환경설정
USER_ID   = "gkfakdrn218@naver.com"
PASSWORD  = "bg2181357!"
BASE_PATH = "/Users/glebang/Desktop/team4"
MYSQL_CFG = dict(user="dbuser", pw="dbpw", host="db.host.com", db="naver")
MONGO_URI = "mongodb://ec2-52-79-243-3.ap-northeast-2.compute.amazonaws.com:27017"
MONGO_DB  = "naver"
MONGO_COLL= "코엑스"

METRICS = [
    {
        "dir": "visitor_data",
        "xpath": "//*[@id=\"gnb\"]/ul/li[4]/div/ul/li[1]/ul/li[2]/a",
        "desc": "지역별방문자수",
        "yearly": True,
        "mysql_t": "visitor"
    },
    {
        "dir": "expense_data",
        "xpath": "//*[@id=\"gnb\"]/ul/li[4]/div/ul/li[2]/ul/li[2]/a",
        "desc": "소비지출유형분석",
        "yearly": True,
        "mysql_t": "expense"
    },
    {
        "dir": "navi_search_data",
        "xpath": "//*[@id=\"gnb\"]/ul/li[4]/div/ul/li[3]/ul/li[3]/a",
        "desc": "검색순위",
        "yearly": True,
        "mysql_t": "ranking"
    },
    {
        "dir": "navigation_data",
        "xpath": "//*[@id=\"gnb\"]/ul/li[4]/div/ul/li[3]/ul/li[2]/a",
        "desc": "검색건수비교",
        "yearly": False,
        "mysql_t": "search"
    },
]

def process_metric(m):
    folder = os.path.join(BASE_PATH, m["dir"])
    os.makedirs(folder, exist_ok=True)

    driver = get_driver(folder)
    login(driver, USER_ID, PASSWORD)
    goto_metric(driver, m["xpath"])
    dates = build_date_ranges(m["yearly"])
    crawl(driver, folder, dates, m["yearly"])
    driver.quit()

    # 정리 → CSV
    sort_by_location_year_month(folder, m["desc"])

    # MySQL 업로드
    to_mysql(BASE_PATH, m["mysql_t"], **MYSQL_CFG)

if __name__ == "__main__":
    for metric in METRICS:
        process_metric(metric)

    # MongoDB에 코엑스 데이터 업로드
    coex_csv = os.path.join(BASE_PATH, "csv", "코엑스.csv")
    to_mongo(coex_csv, MONGO_URI, MONGO_DB, MONGO_COLL)
