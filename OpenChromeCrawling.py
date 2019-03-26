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

    # reCaptcha_iframe_number 가 계속 -1이면 해당 문자열 가진 iframe 찾지 못한 것
    reCaptcha_iframe_number = -1
    for i, iframe in enumerate(iframes):
        try:
            # move to frame one by one
            driver.switch_to.frame(iframes[i])

            # see iframe source
            if string in driver.page_source:
                reCaptcha_iframe_number = i

            # move to default frame
            driver.switch_to.default_content()
        except:
            # move to default frame
            driver.switch_to.default_content()
            print('pass by except : iframes[%d]' % i)
            pass

    if reCaptcha_iframe_number == -1:
        return -1
    else:
        return reCaptcha_iframe_number


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


# 디버깅모드로 크롬 키기, 크롬이 깔린 위치를 지정해 주어야함
os.popen("cd C:\\Program Files (x86)\\Google\\Chrome\\Application && chrome.exe --remote-debugging-port=9222 --user-data-dir=\"C:/ChromeTEMP\"")

# -- setting -- #
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

chrome_driver = "C:\\Users\\LGPC\\Desktop\\상민\\chromedriver"    # chrome_driver 위치
driver = webdriver.Chrome(chrome_driver, options=chrome_options)

# 웹페이지 이동
time.sleep(1)
#driver.get("https://patrickhlauke.github.io/recaptcha/")
time.sleep(1)
# 현재 페이지 내의 모든 iframe 불러오기
iframes = driver.find_elements_by_tag_name('iframe')
find_reCaptcha_string()
