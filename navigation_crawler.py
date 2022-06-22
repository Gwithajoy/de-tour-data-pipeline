# 기본 설정
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import re
import os
from selenium import webdriver

#크롬옵션설정 : 파일 다운로드 위치변경
def get_driver(file_directory):
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : file_directory}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver
#로그인 진행
def login(id, pw, driver):
    driver.implicitly_wait(3) #3초 웨이팅 시간 주기
    driver.get("https://datalab.visitkorea.or.kr/datalab/portal/mbr/getMbrLoginForm.do")
    login_xpath='//*[@id="content"]/div/div/input[3]'
    driver.find_element(by=By.XPATH,value='//*[@id="mbrId"]').send_keys(id) # 자신의 데이터랩 아이디
    driver.find_element(by=By.XPATH,value='//*[@id="mbrPw"]').send_keys(pw) # 자신의 데이터랩 비밀번호
    driver.find_element(by=By.XPATH,value=login_xpath).click()
    time.sleep(2)


def goto_bigdata_navigation_page(way, driver): 
    driver.find_element(by=By.XPATH, value= '//*[@id="gnb"]/ul/li[4]/a').click()  
    big_data = driver.find_element(by=By.XPATH, value= way)
    big_data.send_keys(Keys.ENTER)

    time.sleep(20)

    # go_page = driver.find_element(by=By.XPATH, value='//*[@id="gnb"]/ul/li[4]/div/ul/li[3]/ul/li[3]/a')
    # go_page.click()
    # time.sleep(75) # 최초                             

## 셀레니움 크롤러
### 기간 설정
def set_year_date(driver, is_monthly=False, is_yearly=False):
    if is_monthly:
        data_2018 = list(range(201801,201813))
        data_2019 = list(range(201901,201913))
        data_2020 = list(range(202001,202013))
        data_2021 = list(range(202101,202113))
        data_2022 = list(range(202201,202204))
        years = data_2018 + data_2019 + data_2020 + data_2021 + data_2022
        return years
    if is_yearly:
        data_2018 = (201801,201812)
        data_2019 = (201901,202012)
        data_2020 = (202001,202112)
        data_2021 = (202101,202212)
        data_2022 = (202201,202203)
        years = [data_2018, data_2019, data_2020, data_2021, data_2022]
        return years

def set_location_and_crawling(years, driver, directory, is_monthly=False, is_yearly=False):
    if is_monthly:
        for yearDate in years:
            for column in range(2):
                for row in range(9):
                    # 전국제외 지역설정
                    if column == 0 and row == 0:
                        pass 
                    else:
                        time.sleep(2)
                        driver.find_element(by=By.CSS_SELECTOR, value='#monthStart').send_keys(Keys.COMMAND , "a")
                        time.sleep(0.5)
                        driver.find_element(by=By.CSS_SELECTOR, value="#monthStart").send_keys(f'{yearDate}')
                        time.sleep(0.5)
                        driver.find_element(by=By.CSS_SELECTOR, value='#monthEnd').send_keys(Keys.COMMAND,"a")
                        time.sleep(0.5)
                        driver.find_element(by=By.CSS_SELECTOR, value="#monthEnd").send_keys(f'{yearDate}')
                        time.sleep(0.5)
                        driver.find_element(by=By.CSS_SELECTOR, value="#monthEnd").send_keys(Keys.ENTER)
                        time.sleep(1)
                        driver.find_element(by=By.XPATH, value='//*[@id="vmRegnWrap"]/div[2]/a').send_keys(Keys.ENTER)
                        time.sleep(0.5)
                        path = f"//*[@id='srchNatCdList{column+1}']/a[{row+1}]"
                        location = driver.find_element(by=By.XPATH,value= path).text
                        # 중복다운로드 방지 -> 경로에 있을시, 선택 취소 및 다음 다운로드 실행 
                        if os.path.exists(directory + f'{location}_{yearDate}.xlsx'):
                            driver.find_element(by=By.XPATH, value='//*[@id="popup1"]/div[3]/div/a[1]').send_keys(Keys.ENTER)
                        else:
                            driver.find_element(by=By.XPATH,value= path).click()
                            time.sleep(0.5)                                
                            driver.find_element(by=By.XPATH, value='//*[@id="popup1"]/div[3]/div/a[2]').send_keys(Keys.ENTER)
                            time.sleep(5)
                            driver.find_element(by=By.CSS_SELECTOR, value='#searchWrap > div:nth-child(2) > input').click()
                            time.sleep(20) # 데by=By..CSS_SELECTOR value=이터 불러오는 시간동안 다음단계로 넘어가지 않게 하기 위함
                            driver.find_element(by=By.CSS_SELECTOR, value="#printDiv > div.tab-wrap.clearfix > div.btn-wrap.floatright.btn-option > a").click()
                            time.sleep(0.5)
                            driver.find_element(by=By.CSS_SELECTOR, value='#rdoDataUtilExmn5').click()
                            time.sleep(0.5)
                            driver.find_element(by=By.CSS_SELECTOR, value='#submit').click()
                            print('renaming') # 다른이름으로 저장 작동 확인
                            time.sleep(5)
                            
                            old = directory+"Export.xlsx"
                            new =directory +f'{location}_{yearDate}.xlsx'
                            os.rename(old, new)
                                # 음식 파일 중복 삭제
                        if os.path.exists(f'{location}_음식_{yearDate}.xlsx'):
                            pass
                        else:
                            # 지역선택 
                            driver.find_element(by=By.XPATH, value='//*[@id="vmRegnWrap"]/div[2]/a').send_keys(Keys.ENTER)
                            time.sleep(0.5)
                            # ㅈ지방선택 
                            driver.find_element(by=By.XPATH,value= path).click()
                            time.sleep(0.5)
                            #롹인버트 
                            driver.find_element(by=By.XPATH, value='//*[@id="popup1"]/div[3]/div/a[2]').send_keys(Keys.ENTER)
                            time.sleep(5)
                            # 음식 탭 선택 
                            driver.find_element(by=By.XPATH, value='//*[@id="tabCon1"]/div/div[1]/a[9]').click()
                            time.sleep(10)
                            # 다운로드 선택  
                            driver.find_element(by=By.XPATH, value='//*[@id="printDiv"]/div[1]/div[2]/a').click()
                            time.sleep(1)
                            driver.find_element(by=By.CSS_SELECTOR, value='#rdoDataUtilExmn5').click()
                            time.sleep(0.5)
                            driver.find_element(by=By.CSS_SELECTOR, value='#submit').click()
                            print(f'renaming to {location}_음식_{yearDate}.xlsx') # 다른이름으로 저장 작동 확인
                            time.sleep(5)
                            new =f'{location}_음식_{yearDate}.xlsx'
                            os.rename(old,new)
                        # 숙박 파일 중복 삭제
                        if os.path.exists(f'{location}_숙박_{yearDate}.xlsx'):
                            pass
                        else:
                            # 지역선택 
                            driver.find_element(by=By.XPATH, value='//*[@id="vmRegnWrap"]/div[2]/a').send_keys(Keys.ENTER)
                            time.sleep(0.5)
                            # ㅈ지방선택 
                            driver.find_element(by=By.XPATH,value= path).click()
                            time.sleep(0.5)
                            #롹인버트 
                            driver.find_element(by=By.XPATH, value='//*[@id="popup1"]/div[3]/div/a[2]').send_keys(Keys.ENTER)
                            time.sleep(5)                    
                            driver.find_element(by=By.XPATH, value='//*[@id="tabCon1"]/div/div[1]/a[10]').click()
                            time.sleep(10)
                            driver.find_element(by=By.XPATH, value='//*[@id="printDiv"]/div[1]/div[2]/a').click()
                            time.sleep(1)
                            driver.find_element(by=By.CSS_SELECTOR, value='#rdoDataUtilExmn5').click()
                            time.sleep(0.5)
                            driver.find_element(by=By.CSS_SELECTOR, value='#submit').click()
                            print(f'renaming to {location}_숙박_{yearDate}.xlsx') # 다른이름으로 저장 작동 확인
                            time.sleep(5)
                            new = f'{location}_숙박_{yearDate}.xlsx'
                            os.rename(old,new)                   
                    if yearDate == 202204:
                        break #마지막 자료 다운로드 후 for 문 종료
    if is_yearly :
        for start,end in years:
            for column in range(2):
                for row in range(9):
                    # 전국제외 지역설정
                    if column == 1 and row == 8:
                        pass 
                    else:
                        time.sleep(2)
                        driver.find_element(by=By.CSS_SELECTOR, value='#monthStart').send_keys(Keys.COMMAND, "a")
                        time.sleep(0.5)
                        driver.find_element(by=By.CSS_SELECTOR, value="#monthStart").send_keys(f'{start}')
                        time.sleep(0.5)
                        driver.find_element(by=By.CSS_SELECTOR, value='#monthEnd').send_keys(Keys.COMMAND, "a")
                        time.sleep(0.5)
                        driver.find_element(by=By.CSS_SELECTOR, value="#monthEnd").send_keys(f'{end}')
                        time.sleep(0.5)
                        driver.find_element(by=By.CSS_SELECTOR, value="#monthEnd").send_keys(Keys.ENTER)
                        time.sleep(1)
                        driver.find_element(by=By.XPATH, value='//*[@id="vmRegnWrap"]/div[2]/a').send_keys(Keys.ENTER)
                        time.sleep(0.5)
                        path = f"//*[@id='srchNatCdList{column+1}']/a[{row+1}]"
                        location = driver.find_element(by=By.XPATH,value= path).text
                        # 중복다운로드 방지 -> 경로에 있을시, 선택 취소 및 다음 다운로드 실행 
                        if os.path.exists(directory + f'{location}_{start}_{end}.xlsx'):
                            #지역선택
                            driver.find_element(by=By.XPATH, value='//*[@id="popup1"]/div[3]/div/a[1]').send_keys(Keys.ENTER)
                        else:
                            driver.find_element(by=By.XPATH,value= path).click()
                            time.sleep(0.5)
                            driver.find_element(by=By.XPATH, value='//*[@id="popup1"]/div[3]/div/a[2]').send_keys(Keys.ENTER)
                            time.sleep(5)
                            #driver.find_element(by=By.CSS_SELECTOR, value='#searchWrap > div:nth-child(2) > input').click()
                            #time.sleep(20) # 데by=By..CSS_SELECTOR value=이터 불러오는 시간동안 다음단계로 넘어가지 않게 하기 위함
                            driver.find_element(by=By.CSS_SELECTOR, value="#printDiv > div.tab-wrap.clearfix > div.btn-wrap.floatright.btn-option > a").click()
                            time.sleep(0.5)
                            driver.find_element(by=By.CSS_SELECTOR, value='#rdoDataUtilExmn5').click()
                            time.sleep(0.5)
                            driver.find_element(by=By.CSS_SELECTOR, value='#submit').click()
                            print('renaming') # 다른이름으로 저장 작동 확인
                            time.sleep(5)
                            
                            old = directory+ "Export.xlsx"
                            new =directory+ f'{location}_{start}_{end}.xlsx'
                            os.rename(old, new)
                            if end == 202203:
                                break #마지막 자료 다운로드 후 for 문 종료
                            
 