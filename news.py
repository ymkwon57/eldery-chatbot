from konlpy.tag import Kkma
from konlpy.tag import Twitter
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import re
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
#global users_input
#kkma = Kkma()
twitter = Twitter()

genre = {'정치' : ['정치','정당', '대통령', '의원'],
         '경제' : ['경제', '주식', '집값', '물가'],
         '사회' : ['사회'],
         '생활/문화' : ['생활/문화'],
         '세계' : ['세계'],
         'IT/과학' : ['과학']
        }

def get_user(user_input):
    posed = twitter.pos(user_input)
    posed = [p[0] for p in posed if p[1] in ["Noun","Adjective"]]
    rtn = None
    for p in posed:
        if p in genre.keys():
            rtn = p
            break
        elif p in ["그래", "응", "좋아", "그러렴", "그래주면 고마워", "보여줘"]: #긍정의 표현들
            rtn = 1
        elif p in ["아니", "괜찮아", "별로", "싫어"]: #부정의 표현들
            rtn = 0
    return rtn

def get_top10(genre):
    
    secId = {'정치' : 100,
         '경제' : 101,
         '사회' : 102,
         '생활/문화' : 103,
         '세계' : 104,
         'IT/과학' : 105}
    
    today = datetime.date.today()
    date = today.strftime('%Y%m%d')
    num = secId.get(genre)
    
    r = requests.get('https://news.naver.com/main/ranking/popularDay.nhn?rankingType=popular_day&sectionId='+str(num)+'&date='+str(date)+')')
    s = BeautifulSoup(r.content,"html.parser")
    li = s.find("ol",{"class":"ranking_list"}).findAll("li")
    
    rtn = {}
    link = []
    title = []
    img = []
    
    for i in range(0,10):
        link.append(li[i].find("a")['href'])
        title.append(li[i].find("a")['title'])
        img.append(li[i].find("img")['src'])
    
    rtn['link'] = link
    rtn['title'] = title
    rtn['img'] = img
    
    return rtn

def get_summary(top10, num):
    driver = webdriver.Chrome('C:\\Users\\meeree\\chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument('headless')    
    
    driver.get('https://news.naver.com'+top10['link'][num])
    time.sleep(0.5)
    try:
        driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[3]/div/div[3]/div[2]/div[1]/a').click()
        time.sleep(0.5)
        summary = driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[3]/div/div[3]/div[2]/div[1]/div/div[2]/div[1]').text
    except:
        summary = driver.find_element_by_id("articleBodyContents").text
    driver.close()
    return summary.split('\n\n')



def news_intent(p):
    
    print("====================")

    print('User : ' + p)
    print(get_user(p))

    return_text = ''

    if(len(users_input) == 0):
        # print('Bot : 오늘 뉴스 보실래요?')
        global users_input

        users_input.append(get_user(p))
        print(str(users_input))          
        if(get_user(p) == 1):
            return_text = '어떤 분야의 뉴스를 원하시나요?'
#            return

        elif(get_user(p) == 0):
            #other += 1            
            return_text = '그럼 다른 소식을 추천해드릴까요?'
#            return

        elif(get_user(p) == None):
            #repeat += 1
            return_text = '다시 한번만 말씀해주시겠어요?'
        
        else:
            return_text = '아무것도 아님'

        return return_text
    
    
    #main(p)
    user_before = users_input[-2]
    
    if(user_before == 0 and get_user(p) == 1):
        #users_input = []
        return_text = '다른 추천 소식입니다'
        return return_text

    elif(user_before == 0 and get_user(p) == 0):
        #users_input = []
        return_text = '필요하시면 다시 불러주세요'
        return return_text

#     elif(get_user(p) == None and repeat > 0):
#         print('Bot : 죄송합니다')
        
    elif(user_before == 1 and get_user(p) not in [0,1,None]):
        #user_input = []

        rtn = []

        top10 = get_top10(get_user(p))
        for i,t in enumerate(top10['title']):
            rtn.append(str(i+1) + ' : ' + t)
        
        return str(rtn)
#

if __name__ != '__main__':
    global users_input
    users_input = []