# 크롬이 깔려있는 C:\Program Files (x86)\Google\Chrome\Application 에서
# 명령프롬프트로 >> chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeTEMP"
# chromedriver 가 깔려있어야함

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


# string 문자열이 포함되어있는 iframe 을 찾아 iframes 의 Number 로 사용할 수 있게 해줌
def find_iframe_have_string(string):
    # move to default frame
    driver.switch_to.default_content()

    # iframe_number 가 계속 -1이면 해당 문자열 가진 iframe 찾지 못한 것
    iframe_number = -1
    for i, iframe in enumerate(iframes):
        try:
            # move to frame one by one
            driver.switch_to.frame(iframes[i])
            print(driver.page_source)
            # see iframe source
            if string in driver.page_source:
                iframe_number = i

        except:
            print('pass by except : iframes[%d]' % i)
            pass
    if iframe_number == -1:
        return -1
    else:
        return iframe_number


# element_name에 value를 입력
# 성공 0, 실패 -1
def input_user_info(element_name, value):
    try:
        driver.find_element_by_name(element_name).send_keys(value)
        return 0
    except:
        print("Can't access %s", element_name)
        return -1


def input_Gmarket_user_info():
    print("input_Gmarket_user_info() 실행")
    while True:
        print("-----------------")
        time.sleep(2)
        try:
            # 여기서 속도가 매우 느려지는데 멀티 프로세싱을 통해 단축 시킬 수 있다.
            iframe = driver.find_element_by_xpath("//div[@id='GmktPopLayer']/div[@id='popLayer1']/"
                                                  "div[@id='popLayerContents1']/iframe[@name='popLayerIframe1']")
            driver.switch_to.frame(iframe)
        except:
            print("iframe이 존재하지 않거나 접근할 수 없음")
            continue
        print("ID 입력")
        u_name = 1
        if u_name != 0:
            u_name = input_user_info('u_name', user_info["name"])

        print("생년월일 입력")
        birth_date = 1
        if birth_date != 0:
            birth_date = input_user_info('birth_date', user_info["생년월일"])

        print("휴대폰 번호 입력")
        cellphone_num = 1
        if cellphone_num != 0:
            cellphone_num = input_user_info('cellphone_num', user_info["휴대폰번호"])


user_info = {
    "name": "이상민",
    "국적": "내국인",
    "생년월일": "19950516",
    "성별": "남자",
    "통신사": "SKT",
    "휴대폰번호": "01025012866",
    "자동입력방지문자": "",
}


# 디버깅모드로 크롬 키기, 크롬이 깔린 위치를 지정해 주어야함
# 만약 해당 파일이 chrome 설치 드라이브와 다르면 "C:" 명령어 필요
try:
    os.popen("C: && cd C:\\Program Files (x86)\\Google\\Chrome\\Application && "
             "chrome.exe --remote-debugging-port=9222 --user-data-dir=\"C:\ChromeTEMP\"")
except:
    print("크롬을 찾을 수 없음")
    exit()

# -- setting -- #
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
try:
    chrome_driver = "B:\\sm051\\Desktop\\Break Captcha\\chromedriver"    # chrome_driver 위치
    driver = webdriver.Chrome(chrome_driver, options=chrome_options)

    # 웹페이지 이동, 완전히 로딩되야 넘어가서 시간이 걸림
    driver.get(
        "https://sslmember2.gmarket.co.kr/FindID/FindID?targetUrl=http%3a%2f%2fwww.gmarket.co.kr%2f%3fredirect%3d1")
    input_Gmarket_user_info()
except:
    print("크롬 드라이버를 찾을 수 없음")
    exit()

