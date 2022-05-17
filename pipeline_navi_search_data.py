from sort_and_download import sort_by_location_year_month
import navigation_crawler
from navigation_crawler import get_driver
from navigation_crawler import set_location_and_crawling,login,goto_bigdata_navigation_page, set_year_date
from send_mysql import to_mysql

#다른 모듈의 펑션을 쓰기위한 과정 =>터미널에서와 같이 직접 호출되어 사용될 때는 그 자체로 기능을 수행하고, 동시에 다른 모듈에서 필요한 함수 등을 제공할 수 있다
if __name__ == '__main__':
    #검색순위
    ranking ='//*[@id="gnb"]/ul/li[4]/div/ul/li[3]/ul/li[3]/a'
    path ='/Users/glebang/Desktop/team4/'


    # 지역별 검색순위
    driver= get_driver(path+'navi_search_data')
    login('gkfakdrn218@naver.com','bg2181357!',driver)
    goto_bigdata_navigation_page(ranking, driver)
    years = set_year_date(driver, is_yearly=True)
    set_location_and_crawling(years,driver,path+'navi_search_data/', is_yearly=True)
    sort_by_location_year_month(path+'navi_search_data','검색순위')
    to_mysql(path,'지역별 검색순위(연도별)')
    