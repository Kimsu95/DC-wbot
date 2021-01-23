# -*- coding: utf-8 -*-
# main.py

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import configparser
import random

Config = configparser.ConfigParser()
proxies = []
idlist = []
GALL = []
abc = 0  # 글쓰기 카운터
# URL = 'https://www.dcinside.com'  # 로그인 페이지

# 아이디:패스워드
for line1 in open('./list.txt', 'r'):
    idlist.append(line1)

# 갤러리URL 파일 로드
for line in open('./galls.txt', 'r'):
    GALL.append(line)

# 프록시 파일 로드
for line2 in open('./proxy.txt', 'r'):
    proxies.append(line2)

# config 파일 로드
Config.read('setting.ini', encoding='UTF-8')
setthreads = Config.get('Settings', 'Threads')  # 작성할 글 수
title = Config.get('Thread', 'Title')   # 제목
context = Config.get('Thread', 'Context')   # 본문
temp_id = Config.get('Login', 'Temp_id')  # 임시아이디 ㅇㅇ 추천
temp_pw = Config.get('Login', 'Temp_pw')  # 임시비밀번호

options = webdriver.ChromeOptions()


# nos는 도배방지 우회 숫자
def spambotting(write_url, abc):

    # 프록시 활성화 IP:PORT 또는 HOST:PORT
    # IPv4 HTTP 프록시인 경우
    # options.add_argument('--proxy-server=http://' + proxies[random.randint(0, len(proxies)-1)])
    # SOCKS4 프록시인 경우
    # options.add_argument('--proxy-server=socks4://' + proxies[random.randint(0, len(proxies))])

    # headless 모드
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    # user-agent 변경
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36")

    # 크롬 드라이버 로드
    driver = webdriver.Chrome(executable_path='./chromedriver', options=options)
    driver.implicitly_wait(3)

    # 메인 페이지 로드
    driver.get('https://www.dcinside.com')  # 프록시 zenum.io로 바꿔보기 프록시 연결 오류시 자동 재시도 하기
    # driver.page_source  # 페이지 로딩확인
    time.sleep(5)

    # 로그인 구간
    match_uid = idlist[random.randint(0, len(idlist)-1)].rstrip('\n')  # 'aaa:bbb'
    match_id_split = match_uid.split(':')  # 'aaa', 'bbb'
    match_userid = match_id_split[0]  # 'aaa'
    match_passwd = match_id_split[1]  # 'bbb'
    lo_fail = 0  # 로그인 감지 카운터
    try:
        driver.find_element_by_name('user_id').send_keys(match_userid)
        driver.find_element_by_name("pw").send_keys(match_passwd)
        driver.find_element_by_id('login_ok').click()
        print(f'Login Success {match_uid}')
    except NoSuchElementException:
        print(f'Login failed {match_uid}')
        lo_fail = 1
        return
    # 글작성 페이지 로드
    driver.get(write_url)
    time.sleep(5)

    # 글작성 구간
    # 로그인이 안되었을때 임시 아이디와 비밀번호 이용
    if lo_fail == 1:
        print('Temp login')
        driver.find_element_by_name('name').send_keys(u'{temp_id}')
        driver.find_element_by_name('password').send_keys(temp_pw)
    driver.find_element_by_name('subject').send_keys(title + chr(int(64+random.randint(0, 3)) + abc))  # 제목 입력 + 도배방지 우회 숫자
    driver.find_element_by_id("chk_html").click()  # 본문 html 글쓰기로 변환
    time.sleep(1)

    driver.switch_to.frame(driver.find_element_by_xpath("//iframe[@name='tx_canvas_wysiwyg']"))  # 본문 클릭
    driver.find_element_by_tag_name("body").send_keys(context + chr(int(64+random.randint(0, 3)) + abc))  # 본문 입력 + 도배방지 우회 숫자

    driver.switch_to.default_content()
    driver.find_element_by_class_name("btn_blue").click()  # 등록버튼 클릭
    time.sleep(3)
    print(f'no.{abc} Posted: ' + driver.current_url)
    time.sleep(random.randint(1, 4))
    driver.quit()   # 세션 종료


while abc < int(setthreads):
    for i in range(0, len(GALL)-1):
        spambotting(GALL[i], abc)
    abc = abc + 1  # 글 수 카운트
