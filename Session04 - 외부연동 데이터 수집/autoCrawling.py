#!/usr/bin/env python
# coding: utf-8

# In[6]:


# 라이브러리선언
import pandas as pd
from selenium import webdriver
import time
# 웹브라우저 설정 및 브라우저 팝업
options = webdriver.ChromeOptions()
options.add_argument("window-size=1920*1080")
driverLoc = "../addon/chromedriver.exe"
driver = webdriver.Chrome(executable_path=driverLoc,options=options)
# 브라우저열기
targetUrl = "https://www.kbchachacha.com/"
driver.get(targetUrl)

# 웹페이지 파싱 될때까지 3초 기다림
time.sleep(3)
# 브라우저 내 액션(클릭)
adXpath = '//*[@id="intro01"]/div/div[2]/button'
adBtn = driver.find_element_by_xpath(adXpath)
adBtn.click()
# 웹페이지 파싱 될때까지 3초 기다림
time.sleep(3)
# 브라우저 내 액션(클릭)
ad1Xpath = '//*[@id="popup-main-banner"]/button'
ad1Btn = driver.find_element_by_xpath(ad1Xpath)
ad1Btn.click()
# 웹페이지 파싱 될때까지 3초 기다림
time.sleep(3)

# 브라우저 내 액션(텍스트입력)
from selenium.webdriver.common.keys import Keys

carSearchXpath = "/html/body/div[1]/div[3]/main/div[2]/div[1]/div[2]/div[2]/div[1]/form/fieldset/div/input"

carSearchBox = driver.find_element_by_xpath(carSearchXpath)
# 검색창에 검색어 '코나' 입력
searchKeyword = "코나"

carSearchBox.send_keys(searchKeyword)
# 웹페이지 파싱 될때까지 3초 기다림
time.sleep(3)
# 검색 버튼 클릭
searchXpath = '//*[@id="divDirectSearchWrap"]/div/div[2]/div/a/span'
searchBtn = driver.find_element_by_xpath(searchXpath)
searchBtn.click()

# 페이지 소스 가져오기
pgSource = driver.page_source

# bs4 라이브러리 선언
from bs4 import BeautifulSoup 
import requests

htmlobj = BeautifulSoup(pgSource, "html.parser")
targetParent = htmlobj.find(name="div", attrs={"class":"cs-list02 cs-list02--ratio small-tp generalRegist"})
# 이름 저장
strongTags = targetParent.findAll(name="strong", attrs={"class":"tit"})
# 가격 저장
strongTags1 = targetParent.findAll(name="strong", attrs={"class":"pay"})

# 데이터를 담을 빈 리스트 선언
columnList = []
columnList1 = []

# for이용하여 각각의 열 채우기
for i in range(0,len(strongTags)):
    strongTagsRet = strongTags[i].text.replace("\t","")
    strongTagsRen = strongTagsRet.replace("\n","")
    columnList.append(strongTagsRen)
    
    strongTags1Ret = strongTags1[i].text.replace("\t","")
    strongTags1Ren = strongTags1Ret.replace("\n","")
    columnList1.append(strongTags1Ren)

# zip으로 묶어서 변수에 저장
resultFrame = pd.DataFrame(zip(columnList,columnList1))
# 컬럼명 지정
resultFrame.columns = ["차량등급","가격"]

# SMTP 프로토콜 로드
# 이메일을 간단하게 보낼수 있는 라이브러리 로드
import smtplib
from email.message import EmailMessage

# GMAIL 메일 설정
smtp_gmail = smtplib.SMTP('smtp.gmail.com', 587)
# 서버 연결을 설정하는 단계
smtp_gmail.ehlo()
# 연결을 암호화
smtp_gmail.starttls()

userid = "ganjinam00"

# pickle라이브러리 선언
import pickle

userpw = "mejzuzsdvidhzzoa"

with open('pw.pickle','wb') as handle:
    pickle.dump(userpw,handle,pickle.HIGHEST_PROTOCOL)

with open('pw.pickle','rb') as handle:
    data = pickle.load(handle)

smtp_gmail.login(userid, data)

resultFrame.to_csv("./usedcar_scraping_result.csv",encoding="ms949", index=False)

msg=EmailMessage()
#제목 입력
msg['Subject']="KB차차차 코나 중고차 현황"
#내용 입력
msg.set_content("코나 중고차")
# 보내는 사람
msg['From']='ganjinam00@gmail.com'
# 받는 사람
msg['To'] = 'ganjinam00@naver.com'
# haiteam@kopo.ac.kr

# 첨부파일 추가
file='usedcar_scraping_result.csv'
fp = open(file,'rb')
file_data=fp.read()
msg.add_attachment(file_data,
                   maintype='text',
                   subtype='plain',
                   filename=file)
# 메일 전송
smtp_gmail.send_message(msg)
smtp_gmail.close()


# In[ ]:




