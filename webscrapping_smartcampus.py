# import requests
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver import ActionChains
import csv
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep

# Pageload Strategy 설정 변경 - 시간 절약
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"

#  창 안 띄우기 - 시간 절약
# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')
# options.add_argument('disable-gpu')

# 밑에 있는 세 변수는 사용자 입력으로 처리해야 한다.
Class_num = 10
ID = '20223009'
PW = 'sangwoo6174!'

Weeks = []
Class = []
Lecture = []
Deadline = []
AllData = []


browser = webdriver.Chrome("C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Anaconda3 (64-bit)/chromedriver.exe")
wait = WebDriverWait(browser, 30)

#0 창 크기 최대화
browser.maximize_window()

#1 스캠으로 이동
browser.get("https://class.ssu.ac.kr/")
print("로그인 중...")

#2 로그인 버튼 클릭
browser.find_element(By.CSS_SELECTOR, "#visual > div > div.xn-main-login-container > div.xn-sso-login-btn-wrap > a").click()
#Wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#sLogin > div > div.area_login > form > div > div:nth-child(2) > a")))
print("id pw 입력 중...")

#3 id, pw 입력
browser.find_element(By.CSS_SELECTOR, "#userid").send_keys(ID)
browser.find_element(By.CSS_SELECTOR, "#pwd").send_keys(PW)

#4 로그인창 로그인 버튼 클릭
browser.find_element(By.CSS_SELECTOR, "#sLogin > div > div.area_login > form > div > div:nth-child(2) > a").click()
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#xnm2_content > div.xnp-manual-wrap.xn-mypage > div > div.xn-main-link-wrap.xn-mypage-btn > a > span.manual-text")))
print("마이페이지로 이동 중...")

#5 마이페이지 클릭
browser.find_element(By.CSS_SELECTOR, "#xnm2_content > div.xnp-manual-wrap.xn-mypage > div > div.xn-main-link-wrap.xn-mypage-btn > a").click()

print("마감 정보를 가져오는 중...")


for i in range(Class_num):
    print(i + 1, "번째 과목 정보 가져오는 중...", sep = "")
    class_name_XPATH = '//*[@id="root"]/div/div/div/div[2]/div/div[' + str(i+1) + ']/div[1]/div[1]/div/p' # 과목 이름의 XPATH
    purple_XPATH = '//*[@id="root"]/div/div/div/div[2]/div/div[' + str(i+1) + ']/div[1]/a' # '과목 홈 바로가기'의 xpath
    
    #6-1 '과목 홈 바로가기' 클릭 / 과목 이름 추출
    browser.switch_to.frame("fulliframe")
    wait.until(EC.presence_of_element_located((By.XPATH, purple_XPATH)))
    Class.append(browser.find_element(By.XPATH, class_name_XPATH).text) # 과목 이름 저장
    browser.find_element(By.XPATH, purple_XPATH).click() # 과목 홈 바로가기
   
    #6-2 '강의콘텐츠' 클릭
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "강의콘텐츠")))
    browser.find_element(By.LINK_TEXT, "강의콘텐츠").click()
    
    #6-3 주차수 가져오기
    browser.switch_to.frame("tool_content")
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "xncb-fold-toggle-button"))) #모든 주차 펴기/접기 나올 때까지
  
    weeks = browser.find_elements(By.CLASS_NAME, "xncb-section-header-index-number")
    #6-4 n주차 클릭(최근 것만 할 거면 생략 가능)
    print("len(weeks) = ", len(weeks))
    for j in range(len(weeks)):
        weeks_XPATH = '//*[@id="root"]/div/div[2]/div[' + str(j+1) + ']/header/span'
        if len(browser.find_elements(By.CLASS_NAME, "xncb-section-content-wrapper")) == len(weeks): # 모두 펴짐
            browser.find_element(By.CLASS_NAME, "xncb-fold-toggle-button").click() # 모든 주차 접기
        else:
            browser.find_element(By.CLASS_NAME, "xncb-fold-toggle-button").click() # 모든 주차 펴기
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "xncb-fold-toggle-button"))) # 왜 이게 있어야만 동작하는지 잘 모르겠음
            browser.find_element(By.CLASS_NAME, "xncb-fold-toggle-button").click() # 모든 주차 접기

        browser.find_element(By.XPATH, weeks_XPATH).click() # n주차 클릭
        print(j, "주차 정보 가져오는 중...", sep = "")
    
        #6-5 과목 이름/마감 시간 따오기
#        browser.switch_to.frame("tool_content")
  #      wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#root > div > div.xncb-content-wrapper > div > div > div > header > h2"))) #n주차 나올 때까지
        lectures = browser.find_elements(By.CLASS_NAME, "xncb-component-title")
        
    
        Lecture.append([])
        Deadline.append([])
            
        if(len(lectures) != 0): # 강의가 있는가?
            deadlines = browser.find_elements(By.CLASS_NAME, "xncb-component-periods-date") # 마감 날짜
    
            lectures_index = 0
            for h in deadlines: # 마감 날짜 없으면 실행이 안 되겠쥬?
                if h.text: 
                    Lecture[i].append(lectures[lectures_index].text)
                    Deadline[i].append(h.text[2:])
                    lectures_index += 1
            if lectures_index == 0:
                Lecture[i].append("마감 있는 강의 없음")
                Deadline[i].append("none")
                
        else: 
            Lecture[i].append("강의 없음")
            Deadline[i].append("none")
            
        browser.find_element(By.CLASS_NAME, "xncb-fold-toggle-button").click() #모든 주차 접기

    
    #6-6 다시 마이페이지로 이동
    browser.get("https://class.ssu.ac.kr/mypage")



#7 csv 파일로 정리할 수 있도록 모든 데이터를 AllData에 저장
for i in range(len(Class)):
    print("<과목>", Class[i])
    for j in range(len(Lecture[i])):
        print("    <강의>", Lecture[i][j])
        print("    <마감>", Deadline[i][j])
        

for i in range(len(Class)):
    AllData.append([])
    AllData[i].append(Class[i])
    for j in range(len(Lecture[i])):
        AllData[i].append(Lecture[i][j])
        AllData[i].append(Deadline[i][j])

#8 csv파일 작성
with open('data.csv', 'w', encoding = 'utf-8', newline = '') as f:
    writer = csv.writer(f)
   
    writer.writerows(AllData)
f.close()
