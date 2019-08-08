import urllib.request
#import requests # cx_freeze에서 문제되는거같음
from bs4 import BeautifulSoup

import re
import os
import pickle

def request(url):
   """지정한 url의 웹 문서를 요청하여, 본문을 반환한다."""
   response = urllib.request.urlopen(url)
   byte_data = response.read()
   text_data = byte_data.decode('utf-8')
   return text_data

def get_newNotice():
    URL = 'https://www.hira.or.kr/bbsDummy.do?pgmid=HIRAA020002000100'

    html = request(URL)
    soup = BeautifulSoup(html, 'html.parser')

    info = soup.find_all("table", {"class": "tbl_list"})
    titleInfo = info[0].find_all("td", {"class": "tit_left"})


    URL = URL[:URL.find('?')]
    notice = {}
    for i in range(0, len(titleInfo)):

        tmpNotice = str(titleInfo[i])

        link = tmpNotice[tmpNotice.find('href=') + 6:]
        title = link[link.find('">')+2:link.find('<')]

        link = link[:link.find('">')]
        link = link.replace('amp;','')

        notice[title] = URL+link
    return notice

def UpdateLogFile(notice):
   LogFile = {'Log':notice}
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

         resultlist = []
         for s in newNotice:
            if "수가파일" in s:
               resultlist.append(s)
         newNotice = set(resultlist)

         for info in newNotice:
            sendEmail.append(item + ': ' +  info + ' '+ LogFile[item][info])
         #Update Log File
         file = open(FileName, 'wb')
         pickle.dump(LogFile[str(item)], file)
         file.close()
   return sendEmail

def listToText(NoticeList):
   titleList = ''
   for i in range(0,len(NoticeList)):
      titleList = titleList + NoticeList[i] + '\n'
   return titleList

def EmailService(sendEmail,gmail_user,gmail_pw,from_addr,to_addr):
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

def main():
   notice = get_newNotice()
   sendEmail = UpdateLogFile(notice)
   ## 작성해 주세요
   gmail_user = ''  # 실제 google 로그인할 때 쓰는 ID
   gmail_pw = ''  # 실제 google 로그인할 때 쓰는 Password
   from_addr = ''  # 보내는 사람 주소
   to_addr = ''  # 받는 사람 주소

   EmailService(sendEmail,gmail_user,gmail_pw,from_addr,to_addr)


if __name__ == "__main__":
   main()




