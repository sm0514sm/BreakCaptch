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


def find_reCaptcha_string():
    while True:
        # 현재 페이지 내의 모든 iframe 불러오기
        global iframes
        iframes = driver.find_elements_by_tag_name('iframe')
        time.sleep(3)
        iframe_number = find_iframe_have_string("reCAPTCHA")
        if iframe_number == -1:
            print("reCaptcha frame 찾을 수 없음")
        else:
            # 찾은 iframe_number 의 iframe 으로 이동
            driver.switch_to.frame(iframes[iframe_number])

            reCaptcha_source = driver.page_source                                       # 해당 iframe 의 소스코드 문자열
            soup = BeautifulSoup(reCaptcha_source, "html.parser")                       # BeautifulSoup 클래스로 생성
            divs = soup.findAll('div', {"class": "rc-imageselect-desc-no-canonical"})   # <div class="rc-..."> 인 것들 찾기
            grids = soup.findAll('div', {"class": "rc-imageselect-target"})
            # 3 X 3, 2 X 4 여러개 그림 중에서 특정 단어 일치하는 것들 선택
            if len(divs) == 0:
                divs = soup.findAll('div', {"class": "rc-imageselect-desc"})            # <div class="rc-..."> 인 것들 찾기
                if len(divs) == 0:
                    print("reCaptcha class 찾을 수 없음")
                    continue
            for grid in grids:
                print(grid.get_text())
            for div in divs:                    # 찾은 <div>들 각각
                strongs = div.select('strong')  # <strong> 태그 모두 찾기
                for strong in strongs:
                    print(strong.get_text())
                    return


# element_name에 value를 입력
# 성공 0, 실패 -1
def input_user_info(element_name, value):
    try:
        gmarket_source = driver.page_source  # 해당 iframe 의 소스코드 문자열
        soup = BeautifulSoup(gmarket_source, "html.parser")  # BeautifulSoup 클래스로 생성
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
            u_name = input_user_info('u_name', 'test_id')

        print("생년월일 입력")
        birth_date = 1
        if birth_date != 0:
            birth_date = input_user_info('birth_date', '19950514')

        print("휴대폰 번호 입력")
        cellphone_num = 1
        if cellphone_num != 0:
            cellphone_num = input_user_info('cellphone_num', '01025012866')


# 디버깅모드로 크롬 키기, 크롬이 깔린 위치를 지정해 주어야함
# 만약 해당 파일이 chrome 설치 드라이브와 다르면 "C:" 명령어 필요
try:
    os.popen("C: && cd C:\\Program Files (x86)\\Google\\Chrome\\Application && chrome.exe --remote-debugging-port=9222 --user-data-dir=\"C:\ChromeTEMP\"")
except:
    print("크롬을 찾을 수 없음")
    exit()
print(1)

# -- setting -- #
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_driver = "B:\\sm051\\Desktop\\Break Captcha\\chromedriver"    # chrome_driver 위치
driver = webdriver.Chrome(chrome_driver, options=chrome_options)
print(2)

# 웹페이지 이동, 완전히 로딩되야 넘어가서 시간이 걸림
driver.get("https://sslmember2.gmarket.co.kr/FindID/FindID?targetUrl=http%3a%2f%2fwww.gmarket.co.kr%2f%3fredirect%3d1")
print(3)
input_Gmarket_user_info()

