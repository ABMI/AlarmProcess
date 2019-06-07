# Crolling을 이용한 Alarm Process 개발

## cx_Freeze 설치 (.py ->.exe )
#### https://www.lfd.uci.edu/~gohlke/pythonlibs/#cx_freeze
#### cmd > pip install 다운로드 파일명.확장자

## Code 수정 
#### Crolling.py
<pre>
gmail_user = ''  # 실제 google 로그인할 때 쓰는 ID
gmail_pw = ''  # 실제 google 로그인할 때 쓰는 Password
from_addr = ''  # 보내는 사람 주소
to_addr = ''  # 받는 사람 주소
</pre>


## exe 파일 만들기
#### cmd > python setup.py install


## 스케줄러 등록
- ctrl + R 
- control schedtasks 입력 후 Enter
- 작업 스케줄러 라이브러리 오른쪽 클릭
- 작업 만들기 
- 일반 (권한 설정), 트리거 (공고문 확인 실행 주기), 동작 (만들어진 exe 파일 등록) 설정 후 확인
