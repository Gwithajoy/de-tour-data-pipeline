from sort_and_download import sort_by_location_year_month
import navigation_crawler
from navigation_crawler import get_driver
from navigation_crawler import set_location_and_crawling,login,goto_bigdata_navigation_page, set_year_date
from send_mysql import to_mysql

#다른 모듈의 펑션을 쓰기위한 과정 =>터미널에서와 같이 직접 호출되어 사용될 때는 그 자체로 기능을 수행하고, 동시에 다른 모듈에서 필요한 함수 등을 제공할 수 있다
if __name__ == '__main__':
    search = '//*[@id="gnb"]/ul/li[4]/div/ul/li[3]/ul/li[2]/a'
    path ='/Users/glebang/Desktop/team4/'
    

    #검색건수비교
    driver = get_driver(path+'navigaition_data')
    login('gkfakdrn218@naver.com','bg2181357!', driver)
    goto_bigdata_navigation_page(search, driver)
    years = set_year_date(driver,is_monthly=True)
    set_location_and_crawling(years,driver,path+'navtigation_data/', is_monthly=True)
    sort_by_location_year_month(path+'navigaition_data','검색건수비교')
    to_mysql(path,'지역별 검색건수 비교(월별)')