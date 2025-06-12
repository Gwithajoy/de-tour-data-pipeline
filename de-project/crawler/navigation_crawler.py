import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def get_driver(download_dir: str) -> webdriver.Chrome:
    """크롬 드라이버를 다운로드 디렉토리 지정과 함께 반환"""
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
        'download.default_directory': download_dir
    })
    return webdriver.Chrome(options=options)

def login(driver: webdriver.Chrome, user_id: str, password: str):
    """데이터랩 로그인"""
    driver.implicitly_wait(3)
    driver.get("https://datalab.visitkorea.or.kr/datalab/portal/mbr/getMbrLoginForm.do")
    driver.find_element(By.ID, "mbrId").send_keys(user_id)
    driver.find_element(By.ID, "mbrPw").send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="content"]/div/div/input[3]').click()
    time.sleep(2)

def goto_metric(driver: webdriver.Chrome, metric_xpath: str):
    """대시보드 → 원하는 지표 페이지로 이동"""
    driver.find_element(By.XPATH, '//*[@id="gnb"]/ul/li[4]/a').click()
    driver.find_element(By.XPATH, metric_xpath).send_keys(Keys.ENTER)
    time.sleep(20)

def build_date_ranges(yearly: bool):
    """연별 또는 월별 날짜 리스트 생성"""
    if yearly:
        return [
            (201801, 201812),
            (201901, 202012),
            (202001, 202112),
            (202101, 202212),
            (202201, 202203),
        ]
    else:
        months = []
        for y in range(2018, 2023):
            last = 12 if y < 2022 else 3
            months += list(range(y * 100 + 1, y * 100 + last + 1))
        return months

def crawl(driver: webdriver.Chrome, download_dir: str, date_ranges, yearly: bool):
    """
    실제 데이터 다운로드.
    - yearly=True: date_ranges는 (start, end) 튜플 리스트
    - yearly=False: date_ranges는 YYYYMM 정수 리스트
    """
    for dr in date_ranges:
        start, end = (dr, dr) if not yearly else dr

        # 기간 입력
        driver.find_element(By.CSS_SELECTOR, "#monthStart")\
              .send_keys(Keys.COMMAND, "a", str(start))
        driver.find_element(By.CSS_SELECTOR, "#monthEnd")\
              .send_keys(Keys.COMMAND, "a", str(end), Keys.ENTER)
        time.sleep(1)

        driver.find_element(By.XPATH, '//*[@id="vmRegnWrap"]/div[2]/a')\
              .send_keys(Keys.ENTER)
        time.sleep(0.5)

        # 각 지역(2열×9행) 반복
        for col in (1, 2):
            for row in range(1, 10):
                # 연별 마지막 빈 셀 스킵
                if yearly and col == 2 and row == 9:
                    continue

                cell = f"//*[@id='srchNatCdList{col}']/a[{row}]"
                location = driver.find_element(By.XPATH, cell).text
                fname = f"{location}_{start}" + (f"_{end}" if yearly else "") + ".xlsx"
                out_path = os.path.join(download_dir, fname)

                # 이미 있으면 팝업 닫기
                if os.path.exists(out_path):
                    driver.find_element(By.XPATH,
                        '//*[@id="popup1"]/div[3]/div/a[1]').send_keys(Keys.ENTER)
                    continue

                # 다운로드 버튼들 클릭
                driver.find_element(By.XPATH, cell).click()
                time.sleep(0.5)
                driver.find_element(By.XPATH,
                    '//*[@id="popup1"]/div[3]/div/a[2]').send_keys(Keys.ENTER)
                time.sleep(5)
                driver.find_element(By.CSS_SELECTOR,
                    "#printDiv .btn-option a").click()
                driver.find_element(By.CSS_SELECTOR, "#rdoDataUtilExmn5").click()
                driver.find_element(By.CSS_SELECTOR, "#submit").click()
                time.sleep(5)

                # Export.xlsx → 실제 이름으로 변경
                os.rename(os.path.join(download_dir, "Export.xlsx"), out_path)

        # 연별 마지막 분기까지만
        if yearly and end == 202203:
            break
