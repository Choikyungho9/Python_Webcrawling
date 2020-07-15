#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Step 1. 필요한 모듈과 라이브러리를 로딩합니다.

from bs4 import BeautifulSoup
from selenium import webdriver

import time
import pandas as pd
import xlwt
import math

import random
import os

from selenium.webdriver.support.ui import Select


# In[2]:


#Step 2. 사용자에게 검색어 키워드를 입력 받습니다.
print("=" *80)
print("예제: 대한민국 구석구석 사이트의 여행지 정보 수집하기")
print("=" *80)
query_txt = '대한민국구석구석'
query_area = input('''
 1.서울      2.인천      3.대전      4.대구      5.광주      6.부산      7.울산
 8.세종      9.경기     10.강원     11.충북     12.충남     13.경북     14.경남
15.전북     16.전남     17.제주     18.전체보기 
 
1.위 지역 중 조회하고 싶은 지역의 번호를 입력해 주세요:   ''')


# In[3]:


if query_area == '1' :
    a_value="1"
elif query_area == '2' :
    a_value="2"
elif query_area == '3' :
    a_value="3"
elif query_area == '4' :
    a_value="4"
elif query_area == '5' :
    a_value="5"
elif query_area == '6' :
    a_value="6"
elif query_area == '7' :
    a_value="7"
elif query_area == '8' :
    a_value="8"
elif query_area == '9' :
    a_value="31"
elif query_area == '10' :
    a_value="32"
elif query_area == '11' :
    a_value="33"
elif query_area == '12' :
    a_value="34"
elif query_area == '13' :
    a_value="35"
elif query_area == '14' :
    a_value="36"
elif query_area == '15' :
    a_value="37"
elif query_area == '16' :
    a_value="38"
elif query_area == '17' :
    a_value="39"
elif query_area == '18' :
    a_value="All"


# In[4]:


cnt = int(input('2.크롤링 할 건수는 몇건입니까?: '))
page_cnt = math.ceil(cnt/10)


# In[7]:


# 학습목표 1: 현재 크롤링 시점의 날짜로 폴더 이름을 자동으로 생성하기
 
f_dir = input("3.결과 파일을 저장할 폴더명만 쓰세요(예:C:\\data_science_202007\\notebook\\data\\):")


# In[8]:


# 저장될 파일위치와 이름을 지정합니다
n = time.localtime()
s = '%04d-%02d-%02d-%02d-%02d-%02d' % (n.tm_year, n.tm_mon, n.tm_mday, n.tm_hour, n.tm_min, n.tm_sec)
 
os.makedirs(f_dir+s+'-'+query_txt)
 
ff_name=f_dir+s+'-'+query_txt+'\\'+s+'-'+query_txt+'.txt'
fc_name=f_dir+s+'-'+query_txt+'\\'+s+'-'+query_txt+'.csv'
fx_name=f_dir+s+'-'+query_txt+'\\'+s+'-'+query_txt+'.xls'


# In[9]:


#Step 3. 크롬 드라이버를 사용해서 웹 브라우저를 실행합니다.
 
s_time = time.time( )
 
path = "C:\data_science_202007\datadown/chromedriver.exe"
driver = webdriver.Chrome(path)
 
driver.get('https://korean.visitkorea.or.kr')
 
time.sleep(random.randrange(2,5))  # 2 - 5 초 사이에 랜덤으로 시간 선택


# In[ ]:


#코로나 얼럿창 있을 경우 닫기 클릭하기 
try :
    driver.find_element_by_xpath('//*[@id="safetyStay1"]/div/div/div/button').click()
except :
    print("코로나 창이 없습니다")


# In[ ]:


driver.find_element_by_xpath("""//*[@id="btnMenu"]""").click()
driver.find_element_by_link_text('''여행지''').click()
time.sleep(3)


# In[ ]:


driver.find_element_by_xpath("""//*[@id="areaselect"]""").click()
element1 = Select(driver.find_element_by_id("areaselect"))
element1.select_by_value(a_value)

time.sleep(2)


# In[ ]:


# Step 5: 사용자 요청 건수가 실제 검색 건수보다 많을 경우
# 실제 검색 건수로 리셋하기
html = driver.page_source
soup = BeautifulSoup(html,'html.parser')


# In[ ]:


r_cnt = soup.find('div', 'total_check').find('span').get_text()

r_cnt2 = r_cnt.replace(",","")
search_cnt = int(r_cnt2)


# In[ ]:


print("전체 검색 결과 건수 :", search_cnt,"건")
print("실제 최종 출력 건수 :", cnt)


# In[ ]:


print("\n")
page_cnt = math.ceil(cnt/10)
print("크롤링 할 총 페이지 번호: ",page_cnt)
print("="*80)


# In[ ]:


# Step 6. 페이지를 변경하면서 사용자가 요청한 건수만큼 내용을 추출하여 파일에 저장하기
no2=[] #게시글 번호 컬럼
contents=[] #게시글 내용 컬럼
no = 1


# In[ ]:


for x in range(1, page_cnt+1):
    print("%s 페이지 내용 수집 시작합니다 ========================" %x)
    
    for i in range(1, 11):
        if no > cnt:
            break
            
        #각 게시글의 제목 누르기
        driver.find_element_by_xpath("""//*[@id="contents"]/div[2]/div[1]/ul/li[%s]/div[2]/div/a"""%i).click()
        time.sleep(2)
        
        html = driver.page_source #상세페이지 HTML 가져오기
        soup = BeautifulSoup(html, 'html.parser')
        content_list = soup.find('div','wrap_contView') #내용부분 태그찾기
        con_1 = content_list.find('p').get_text() # 내용태그에서 텍스트만 가져온다.
        print(no, ': ', con_1) #번호와, 추출한 데이터 출력한다.
        print("\n")
        
        f=open(ff_name, 'a', encoding='UTF-8')
        f.write(str(no) + ': ' + str(con_1) + "\n") #추출한 데이터 텍스트 파일에 저장
        f.close()
        
        no2.append(no)
        contents.append(con_1)
        
        driver.back() #뒤로 돌아가기 기능(목록 페이지로 이동)
        time.sleep(2) #페이지 이동하는 동안 2초정도 쉰다.
        
        no += 1
        
    if x > page_cnt+1 :
        break
        
    x += 1
    
    if (x%5==1):
        driver.find_element_by_link_text('''다음''').click()
    else:
        driver.find_element_by_link_text('''%s''' %x).click() #다음 페이지번호 클릭
    time.sleep(2)


# In[ ]:


# Step 7. 출력 결과를 표(데이터 프레임) 형태로 만들어 csv,xls 형식으로 저장하기
korea = pd.DataFrame()
korea['번호']=no2
korea['내용']=contents
        
# csv 형태로 저장하기
korea.to_csv(fc_name,encoding="utf-8-sig",index=False)
 
# 엑셀 형태로 저장하기
korea.to_excel(fx_name,index=False)
 
e_time = time.time( )     # 검색이 종료된 시점의 timestamp 를 지정합니다
t_time = e_time - s_time
 
 
# Step 8. 요약정보 보여주기
print("\n") 
print("=" *80)
print("총 소요시간은 %s 초 입니다 " %round(t_time,1))
print("파일 저장 완료: txt 파일명 : %s " %ff_name)
print("파일 저장 완료: csv 파일명 : %s " %fc_name)
print("파일 저장 완료: xls 파일명 : %s " %fx_name)
print("=" *80)
 
driver.close( )


# In[ ]:




