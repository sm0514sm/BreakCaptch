# 크롬이 깔려있는 C:\Program Files (x86)\Google\Chrome\Application 에서
# 명령프롬프트로 >> chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeTEMP"
# chromedriver 가 깔려있어야함

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select


# element_name 에 value 를 입력
# 성공 1, 실패 0
def input_user_info(element_name, value):
    try:
        driver.find_element_by_name(element_name).send_keys(value)
        return 1
    except BaseException as e:
        print(e)
        return 0

def get_Captcha_image():
    print("get_Captcha_image() 실행")
    try:
        driver.find_element_by_id("captcha_img").screenshot("captcha.png")
        driver.find_element_by_class_name("bt_sound").click()
        return 1
    except BaseException as e:
        print(e)
        return 0

def input_Gmarket_user_info():
    print("input_Gmarket_user_info() 실행")
    try:
        # TODO 여기서 속도가 매우 느려지는데 멀티 프로세싱을 통해 단축 시킬 수 있다.
        iframe = driver.find_element_by_xpath("//div[@id='GmktPopLayer']/div[@id='popLayer1']/"
                                              "div[@id='popLayerContents1']/iframe[@name='popLayerIframe1']")
        driver.switch_to.frame(iframe)
    except BaseException as e:
        print(e)
        return

    if not get_Captcha_image():
        print("Captcha 이미지 다운로드 실패")

    print("user_info 입력")

    if not input_user_info('u_name', user_info["이름"]):
        print("이름 입력 실패")

    select = Select(driver.find_element_by_name('naSelect'))
    select.select_by_visible_text(user_info["국적"])

    if not input_user_info('birth_date', user_info["생년월일"]):
        print("생년월일 입력 실패")

    if user_info["성별"] == "남자":
        driver.find_element_by_id("gender_male").click()
    else:
        driver.find_element_by_id("gender_female").click()

    select = Select(driver.find_element_by_name('carrier_sel'))
    select.select_by_visible_text(user_info["통신사"])

    if not input_user_info('cellphone_num', user_info["휴대폰번호"]):
        print("휴대폰 번호 입력 실패")


def input_cellphone_user_info():
    print("input_cellphone_user_info() 실행")
    # try:
    #     # TODO 여기서 속도가 매우 느려지는데 멀티 프로세싱을 통해 단축 시킬 수 있다.
    #     iframe = driver.find_element_by_xpath("//div[@id='GmktPopLayer']/div[@id='popLayer1']/"
    #                                           "div[@id='popLayerContents1']/iframe[@name='popLayerIframe1']")
    #     driver.switch_to.frame(iframe)
    # except:
    #     print("iframe 이 존재하지 않거나 접근할 수 없음")
    #     return
    #
    # print("user_info 입력")
    #
    if not input_user_info('smsName', user_info["이름"]):
         print("이름 입력 실패")
    #
    # select = Select(driver.find_element_by_name('naSelect'))
    # select.select_by_visible_text(user_info["국적"])
    #
    # if not input_user_info('birth_date', user_info["생년월일"]):
    #     print("생년월일 입력 실패")
    #
    # print("성별 선택")
    # if user_info["성별"] == "남자":
    #     driver.find_element_by_id("gender_male").click()
    # else:
    #     driver.find_element_by_id("gender_female").click()
    #
    # select = Select(driver.find_element_by_name('carrier_sel'))
    # select.select_by_visible_text(user_info["통신사"])
    #
    # if not input_user_info('cellphone_num', user_info["휴대폰번호"]):
    #     print("휴대폰 번호 입력 실패")


def set_user_info(name, nationality, birth_date, gender, mobile_carrier, mobile_number, string):
    global user_info
    if name:
        user_info["이름"] = name
    if nationality:
        user_info["국적"] = nationality
    if birth_date:
        user_info["생년월일"] = birth_date
    if gender:
        user_info["성별"] = gender
    if mobile_carrier:
        user_info["통신사"] = mobile_carrier
    if mobile_number:
        user_info["휴대폰번호"] = mobile_number


user_info = {
    "이름": "이상민",
    "국적": "외국인",
    "생년월일": "19950516",
    "성별": "남자",
    "통신사": "LGU알뜰폰",
    "휴대폰번호": "01025012866",
    "자동입력방지문자": "",
}
driver = None


def do_crawling():

    # 디버깅모드로 크롬 키기, 크롬이 깔린 위치를 지정해 주어야함
    # 만약 해당 파일이 chrome 설치 드라이브와 다르면 "C:" 명령어 필요
    try:
        os.popen("C: && cd C:\\Program Files (x86)\\Google\\Chrome\\Application && "
                 "chrome.exe --remote-debugging-port=9222 --user-data-dir=\"C:\ChromeTEMP\"")
    except BaseException as e:
        print("*Error :", e)
        exit()

    # -- setting -- #
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    try:
        global driver
        chrome_driver = "C:/Users/Cho/Documents/BreakCaptcha/chromedriver.exe"    # chrome_driver 위치
        driver = webdriver.Chrome(chrome_driver, options=chrome_options)

        # 웹페이지 이동, 완전히 로딩되야 넘어가서 시간이 걸림
        # driver.get(
        #    "https://sslmember2.gmarket.co.kr/FindID/FindID?targetUrl=http%3a%2f%2fwww.gmarket.co.kr%2f%3fredirect%3d1")
        while True:
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[-1])
            driver.implicitly_wait(3)
            current_url = driver.current_url
            old_url = ""
            print(current_url)
            # TODO 계속 실행됨
            if old_url != current_url:
                if "sslmember2.gmarket.co.kr/FindID" in current_url:
                    input_Gmarket_user_info()
                elif "mobile-ok.com/SimplePop" in current_url:
                    input_cellphone_user_info()
            old_url = current_url

    except BaseException as e:
        print("*Error :", e)
        exit()

