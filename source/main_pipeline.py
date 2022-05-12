from sort_and_download import sort_by_location_year_month
import navigation_crawler
from navigation_crawler import get_driver
from navigation_crawler import set_location_and_crawling,login,goto_bigdata_navigation_page, set_year_date

#다른 모듈의 펑션을 쓰기위한 과정 =>터미널에서와 같이 직접 호출되어 사용될 때는 그 자체로 기능을 수행하고, 동시에 다른 모듈에서 필요한 함수 등을 제공할 수 있다
if __name__ == '__main__':
    #지역별방문자수 비교
    visitor ='//*[@id="gnb"]/ul/li[4]/div/ul/li[1]/ul/li[2]/a'
    #관광지별 소비지출유형분석
    expense ='//*[@id="gnb"]/ul/li[4]/div/ul/li[2]/ul/li[2]/a'
    #검색순위
    ranking ='//*[@id="gnb"]/ul/li[4]/div/ul/li[3]/ul/li[3]/a'
    #검색건수비교
    search = '//*[@id="gnb"]/ul/li[4]/div/ul/li[3]/ul/li[2]/a'
    path ='/Users/glebang/Desktop/team4'
    #지역별방문자수 과정
    driver = get_driver(path + 'visitor_data')
    login('gkfakdrn218@naver.com','bg2181357!',driver)
    goto_bigdata_navigation_page(visitor,driver)
    years = set_year_date(driver, is_yearly=True)
    set_location_and_crawling(years, driver, path + 'visitor_data/',is_yearly=True)
    sort_by_location_year_month(path+'visitor_data','지역별방문자수')
    
    #관광지별 소비지출유형분석
    driver =get_driver(path+'expense_data')
    login('gkfakdrn218@naver.com','bg2181357!',driver)
    goto_bigdata_navigation_page(expense, driver)
    years = set_year_date(driver, is_yearly=True)
    set_location_and_crawling(years, driver, path+'expense_data/', is_yearly=True)
    sort_by_location_year_month(path+'expense_data','소비지출유형분석')
    
    # #검색순위
    driver= get_driver(path+'navi_search_data')
    login('gkfakdrn218@naver.com','bg2181357!',driver)
    goto_bigdata_navigation_page(ranking, driver)
    years = set_year_date(driver, is_yearly=True)
    set_location_and_crawling(years,driver,path+'navi_search_data/', is_yearly=True)
    sort_by_location_year_month(path+'navi_search_data','검색순위')
    
    #검색건수비교
    driver = get_driver(path+'navigaition_data')
    login('gkfakdrn218@naver.com','bg2181357!', driver)
    goto_bigdata_navigation_page(search, driver)
    years = set_year_date(driver,is_monthly=True)
    set_location_and_crawling(years,driver,path+'navtigation_data/', is_monthly=True)
    sort_by_location_year_month(path+'navigaition_data','검색건수비교')
    