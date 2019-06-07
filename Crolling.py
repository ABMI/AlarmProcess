# pip install requests # 파이썬에 내장된 urllib 모듈을 편하게 사용하게 해 줌.
# pip install beautifulsoup4 # html, xml 파싱

import urllib.request
#import requests # cx_freeze에서 문제되는거같음
from bs4 import BeautifulSoup

import re
import os
import pickle

# from datetime import datetime
# now = datetime.now()
# today = now.strftime("%Y-%m-%d")
# today = '2019-05-16'

# 알람 오게 지정할 단어
#drugKeyword = ['신약']
#procedureKeyword = ['신의료기술평가위원회']

# def get_html(url):
#    _html = ""
#    resp = requests.get(url)
#    if resp.status_code == 200:
#       _html = resp.text
#    return _html
## 작성해 주세요
gmail_user = ''  # 실제 google 로그인할 때 쓰는 ID
gmail_pw = ''  # 실제 google 로그인할 때 쓰는 Password
from_addr = ''  # 보내는 사람 주소
to_addr = ''  # 받는 사람 주소

def request(url):
   """지정한 url의 웹 문서를 요청하여, 본문을 반환한다."""
   response = urllib.request.urlopen(url)
   byte_data = response.read()
   text_data = byte_data.decode('utf-8')
   return text_data

#NECA(신의료 기술 평가 사업 본부) # 신 시술 공고
def get_newProcedureNotice():
   frontLink = 'https://nhta.neca.re.kr'
   URL = 'https://nhta.neca.re.kr/nhta/notice/nhtaU0401L.ecg'

   html = request(URL)
   soup = BeautifulSoup(html, 'html.parser')

   info = soup.find_all("div", {"class": 'table_list01 mt10 noti'})
   tableInfo = info[0].find_all("tbody")
   textInfo = tableInfo[0].find_all("tr")

   notice = {}
   for i in range(0, len(textInfo)):
      titleInfo = textInfo[i].find_all('a')
      dateInfo = textInfo[i].find_all('td', {'class': 'date'})
      # title
      tmpTitle = str(titleInfo)

      # link 전처리
      link = tmpTitle[tmpTitle.find('href=') + 6:tmpTitle.find('\">')]
      link = link.replace('¤t', '&current')
      # title 전처리
      title = tmpTitle[tmpTitle.find('\">') + 6:tmpTitle.find('</a>')]
      title = re.sub('[\n\t\r ]{1,}', ' ', title)
      # date
      tmpDate = str(dateInfo)
      date = tmpDate[tmpDate.find('date') + 6:tmpDate.find('</td>')]

      notice[title+date] = frontLink + link

   return notice


# 식품 의약품 안전처 # 신약 공고
def get_newDrugNotice():
   frontLink = 'http://www.mfds.go.kr/brd/m_76/'
   URL = 'http://www.mfds.go.kr/brd/m_76/list.do?page=1&srchFr=&srchTo=&srchWord=&srchTp=&itm_seq_1=0&itm_seq_2=0&multi_itm_seq=0&company_cd=&company_nm='

   html = request(URL)
   soup = BeautifulSoup(html, 'html.parser')

   info = soup.find_all("div", {"class": "bbs_list01"})
   titleInfo = info[0].find_all("div", {"class": "center_column"})
   dateInfo = info[0].find_all("div", {"class": "right_column"})

   notice = {}
   for i in range(0, len(titleInfo)):
      tmpDate = str(dateInfo[i])
      date = tmpDate[tmpDate.find('right_column') + 14:tmpDate.find('</div>')]

      tmpNotice = titleInfo[i].find_all("a", {'class', 'title'})
      tmpNotice = str(tmpNotice)

      link = tmpNotice[tmpNotice.find('href=') + 8:tmpNotice.find('title=') - 2]
      title = tmpNotice[tmpNotice.find('title=') + 7:tmpNotice.find('자세히보기')]

      notice[title+date] = frontLink+link

   return notice

def listToText(NoticeList):
   titleList = ''
   for i in range(0,len(NoticeList)):
      titleList = titleList + NoticeList[i] + '\n'
   return titleList

#결과 저장
#Log 파일 설정 해주기
LogFile = {'식품의약품안전처':get_newDrugNotice(),'NECA(신의료기술사업본부)':get_newProcedureNotice()}
# test 용
#LogFile = {'식품의약품안전처': {'새로운 페이지':'www.nwnww.com','이것도':'wewe.coms'}, 'NECA(신의료기술사업본부)': {' 2018년 제10차 신의료기술평가위원회 개최결과 (10.26.) 2018.11.20': 'https://nhta.neca.re.kr/nhta/notice/nhtaU0400V.ecg?seq=2500&currentPage=1&amp;boardno=all','new Notice':'www.newnew.com'}}
sendEmail = []
for item in LogFile.keys():
   FileName = os.getcwd()+'\\' + item + '.txt'
   if not (os.path.exists(FileName)):
      file = open(FileName, 'wb')
      pickle.dump(LogFile[str(item)],file)
      file.close()
   else:
      file = open(FileName, 'rb')
      content  = pickle.load(file)
      file.close()
      newNotice = set(LogFile[item].keys()) - set(content.keys())
      for notice in newNotice:
         sendEmail.append(item + ': ' +  notice + ' '+ LogFile[item][notice])
      #새 공고로 치환
      file = open(FileName, 'wb')
      pickle.dump(LogFile[str(item)], file)
      file.close()

sendEmail = listToText(sendEmail)
title = '새 공고가 있습니다.'
body = sendEmail

if sendEmail != '':
   #메일 보내기

   # 메일 전송
   import smtplib
   from email.mime.multipart import MIMEMultipart
   from email.mime.text import MIMEText

   msg = MIMEMultipart('alternative')
   msg['From'] = from_addr
   msg['To'] = to_addr
   msg['Subject'] = title  # 제목
   msg.attach(MIMEText(body, 'plain', 'utf-8'))  # 내용 인코딩
   ######################## # https://www.google.com/settings/security/lesssecureapps # Make sure less_secure_apps select 'use' ########################
   try:
      server = smtplib.SMTP("smtp.gmail.com", 587)
      server.ehlo()
      server.starttls()
      server.login(gmail_user, gmail_pw)
      server.sendmail(from_addr, to_addr, msg.as_string())
      server.quit()
      print('successfully sent the mail')
   except BaseException as e:
      print("failed to send mail", str(e))
else:
   print('new notice is not exists')

