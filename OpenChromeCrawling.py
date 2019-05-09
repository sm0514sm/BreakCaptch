# 크롬이 깔려있는 C:\Program Files (x86)\Google\Chrome\Application 에서
# chromedriver 가 깔려있어야함

import time
import urllib.request
import selenium
from ImagePreProcessing import OneImageProcessingAndML
from AudioPreprocessing import OneSoundProcessingAndML
from selenium import webdriver
from selenium.webdriver.support.ui import Select


successInput = False


# element_name 에 value 를 입력
# 성공 1, 실패 0
def input_element(ele_name, value):
    try:
        ele = driver.find_element_by_id(ele_name)
        ele.send_keys(value)
        if ele_name == "captchaCode":
            ele.click()
        return 1
    except BaseException as e:
        print(e)
        return 0


# 자동입력방지문자의 이미지와 음성 파일을 다운로드
def get_Captcha_image(site):
    print("get_Captcha_image() 실행")
    try:
        if site == "Gmarket":
            driver.find_element_by_id("captcha_img").screenshot("captcha.png")
            captcha = driver.find_element_by_id("captcha")
            value = captcha.get_attribute("value")
            url = "https://sslmember2.gmarket.co.kr/GCaptcha/CurrentSound?encValue="+value
            urllib.request.urlretrieve(url, "captcha.wav")
        elif site == "Auction":
            # 이미지는 사이트내의 객체를 바로 가져오지만 학습시킨 이미지 height 과 달라 resizing 필요
            driver.find_element_by_id("gCapImage").screenshot("captcha.png")
            # 음성의 경우, url 을 알아내서 접근하는 것인데 옥션의 경우, 직접접근을 막아두어서 접근 불가
            captcha = driver.find_element_by_id("hidCaptcha")
            value = captcha.get_attribute("value")
            url = "https://memberssl.auction.co.kr/GCaptcha/CurrentSound?encValue=" + value
            urllib.request.urlretrieve(url, "captcha.wav")
        elif site == "PASS":
            pass
        else:
            print("*Error : 알 수 없는 페이지")
        return 1
    except BaseException as e:
        print("*get_Captcha_image:", e)
        return 0


# HTML 가져올 element 의 tag 이름을 설정함
def set_element_name(site, name, nationality, birth_date, gender_male, gender_female,
                     mobile_carrier, mobile_number, captcha_character):
    global element_name
    if site == element_name["사이트"]:  # 기존것과 동일하다면 스킵
        return
    element_name["사이트"] = site
    element_name["이름"] = name
    element_name["국적"] = nationality
    element_name["생년월일"] = birth_date
    element_name["성별남"] = gender_male
    element_name["성별여"] = gender_female
    element_name["통신사"] = mobile_carrier
    element_name["휴대폰번호"] = mobile_number
    element_name["자동입력방지문자"] = captcha_character


# 사용자 정보 + 자동입력방지문자 입력
def input_user_info(site_name):
    global successInput
    if site_name == "Gmarket":
        print("Gmarket 실행")
        try:
            iframe = driver.find_element_by_id("popLayerIframe1")
            driver.switch_to.frame(iframe)
        except selenium.common.exceptions.NoSuchElementException as e:
            print("*Error : 입력가능한 Gmarket frame 없음")
            successInput = False
            return
        set_element_name("Gmarket", "u_name", "naSelect", "birth_date", "gender_male", "gender_female",
                         "carrier_sel", "cellphone_num", "captchaCode")
    elif site_name == "Auction":
        print("Auction 실행")
        driver.find_element_by_class_name("bt_sound").click()   # 옥션의 경우, 사운드 버튼을 클릭해야지 얻을 수 있음
        # 옥션은 새창으로 팝업되기때문에 iframe 바꿀 필요 없음
        set_element_name("Auction", "name", "naSelect", "ssnLeft8", "sexSelect1", "sexSelect2",
                         "carrierType", "cpNo", "captchaCode")
    elif site_name == "PASS":
        print("PASS 휴대폰 본인확인 실행")
        # 옥션은 새창으로 팝업되기때문에 iframe 바꿀 필요 없음
        set_element_name("PASS", "smsName", "native", "smsBirth", "m_sel", "fm_sel",
                         None, "smsMobileNum", "s_secureText")
        pass
    else:
        print("*Error : 알 수 없는 사이트")
        return

    if successInput is False:
        if not get_Captcha_image(site_name):
            print("Captcha 이미지 다운로드 실패")
        # user_info["자동입력방지문자"] = OneImageProcessingAndML()     # 이미지로 머신러닝
        user_info["자동입력방지문자"] = OneSoundProcessingAndML()       # 사운드로 머신러닝
        print("user_info 입력")

        if not input_element(element_name["이름"], user_info["이름"]):
            print("이름 입력 실패")
            return

        select = Select(driver.find_element_by_id(element_name["국적"]))
        select.select_by_visible_text(user_info["국적"])

        if not input_element(element_name["생년월일"], user_info["생년월일"]):
            print("생년월일 입력 실패")
            return

        if element_name["성별남"] is not None and element_name["성별여"] is not None:
            try:
                if user_info["성별"] == "남자":
                    driver.find_element_by_id(element_name["성별남"]).click()
                else:
                    driver.find_element_by_id(element_name["성별여"]).click()
            except selenium.common.exceptions.NoSuchElementException:
                if user_info["성별"] == "남자":
                    driver.find_element_by_class_name(element_name["성별남"]).click()
                else:
                    driver.find_element_by_class_name(element_name["성별여"]).click()

        if element_name["통신사"] is not None:
            select = Select(driver.find_element_by_id(element_name["통신사"]))
            select.select_by_visible_text(user_info["통신사"])

        if not input_element(element_name["휴대폰번호"], user_info["휴대폰번호"]):
            print("휴대폰 번호 입력 실패")
            return

        if not input_element(element_name["자동입력방지문자"], user_info["자동입력방지문자"]):
            print("자동입력방지문자 입력 실패")
            return
        successInput = True


# 유저 정보를 설정함
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


element_name = {
    "사이트": "Gmarket",
    "이름": "u_name",
    "국적": "naSelect",
    "생년월일": "birth_date",
    "성별남": "gender_male",
    "성별여": "gender_female",
    "통신사": "carrier_sel",
    "휴대폰번호": "cellphone_num",
    "자동입력방지문자": "captchaCode",
}
user_info = {
    "이름": "이상민",
    "국적": "외국인",
    "생년월일": "19950516",
    "성별": "여자",
    "통신사": "KT알뜰폰",
    "휴대폰번호": "01025012866",
    "자동입력방지문자": "",
}
driver = None


def do_crawling():
    try:
        global driver
        # chrome_driver = "C:/Users/Cho/Documents/BreakCaptcha/chromedriver.exe"    # chrome_driver 위치
        chrome_driver = "C:/Users/LGPC/Desktop/상민/BreakCaptcha/chromedriver.exe"  # chrome_driver 위치
        driver = webdriver.Chrome(chrome_driver)

        while True:
            try:
                global successInput
                time.sleep(1)
                current_url = driver.current_url
                driver.switch_to.window(driver.window_handles[-1])
                print("-----------------------------------------------------")
                print("*url : ", driver.current_url)
                print("*successInput :", successInput)
                if "sslmember2.gmarket.co.kr/FindID" in current_url:
                    input_user_info("Gmarket")
                elif "Common/CustomizedVerification" in current_url:
                    input_user_info("Auction")
                elif "mobile-ok.com/SimplePop" in current_url:
                    input_user_info("PASS")
            except selenium.common.exceptions.NoSuchWindowException as e:
                driver.switch_to.window(driver.window_handles[-1])
                print("윈도우 바꿈")
            except BaseException as e:
                print(e)
    except BaseException as e:
        print("*Error :", e)
        driver.close()
        exit()

