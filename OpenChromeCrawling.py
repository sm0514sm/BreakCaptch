# 크롬이 깔려있는 C:\Program Files (x86)\Google\Chrome\Application 에서
# chromedriver 가 깔려있어야함

import time
import urllib.request
import requests
import selenium
from ImagePreProcessing import OneImageProcessingAndML
from AudioPreprocessing import OneSoundProcessingAndML
from selenium import webdriver
from selenium.webdriver.support.ui import Select



# Highlights (blinks) a Selenium Webdriver element
def highlight(element):
    driver = element._parent

    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, s)
    apply_style("background: yellow;")


class Crawler:
    def __init__(self):
        self.successInput = False
        self.element_name = {
            "사이트": "Gmarket",
            "이름": "u_name",
            "국적": "naSelect",
            "생년월일": "birth_date",
            "성별남": "gender_male",
            "성별여": "gender_female",
            "통신사": "carrier_sel",
            "휴대폰번호": "cellphone_num",
            "자동입력방지문자": "captchaCode",
            "모두동의": None,
        }
        self.user_info = {
            "이름": "이상민",
            "국적": "외국인",
            "생년월일": "19950516",
            "성별": "여자",
            "통신사": "KT알뜰폰",
            "휴대폰번호": "01025012866",
            "자동입력방지문자": "",
        }
        self.driver = None
        self.driver_path = ""

    # element_name 에 value 를 입력
    # 성공 1, 실패 0
    def input_element(self, ele_name, value):
        try:
            ele = self.driver.find_element_by_id(ele_name)
            ele.send_keys(value)
            highlight(ele)
            if ele_name == "captchaCode":
                ele.click()
            return 1
        except BaseException as e:
            print(e)
            return 0

    # 자동입력방지문자의 이미지와 음성 파일을 다운로드
    def get_Captcha_image(self, site):
        print("get_Captcha_image() 실행")
        try:
            if site == "Gmarket":
                self.driver.find_element_by_id("captcha_img").screenshot("captcha.png")
                captcha = self.driver.find_element_by_id("captcha")
                value = captcha.get_attribute("value")
                url = "https://sslmember2.gmarket.co.kr/GCaptcha/CurrentSound?encValue="+value
                urllib.request.urlretrieve(url, "captcha.wav")
            elif site == "Auction":
                # 이미지는 사이트내의 객체를 바로 가져오지만 학습시킨 이미지 height 과 달라 resizing 필요
                self.driver.find_element_by_id("gCapImage").screenshot("captcha.png")
                # 음성의 경우, url 을 알아내서 접근하는 것인데 옥션의 경우, 직접접근을 막아두어서 접근 불가
                captcha = self.driver.find_element_by_id("hidCaptcha")
                value = captcha.get_attribute("value")
                url = "https://memberssl.auction.co.kr/Common/GCaptcha/GCaptchaService.aspx?mtype=S&encvalue=" + value
                referer = self.driver.current_url
                cookie = 'pcid=1558356403914; cguid=11558356403737005811000000; sguid=31558356403737005811274000; pguid=21558356403737005811010000; WMONID=P_D_sREpAj2; RPM=BT%3DL1558356410365; AGP=fccode=AH41; channelcode=0C42; ssguid=315585000520530047312740000; gen=1KRgroBk1H45VAtrQ0OlmeMHzynS41CcSzdnr8/0NuK5d/d556P5lMX4OjtRumv2AZID/DSU5M/zX+/xQUIxB7pPGqceA1rBRT3eoAB16fY='
                header = {
                    'Host': 'memberssl.auction.co.kr',
                    'Connection': 'keep-alive',
                    'Accept-Encoding': 'identity;q=1, *;q=0',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
                    'chrome-proxy': 'frfr',
                    'Accept': '*/*',
                    'Referer': referer,
                    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Cookie': cookie,
                    'Range': 'bytes=0-',
                }
                r = requests.get(url=url, headers=header, verify=False)
                print(r.content)
                open("captcha.wav", 'wb').write(r.content)
            elif site == "PASS":
                pass
            else:
                print("*Error : 알 수 없는 페이지")
            return 1
        except BaseException as e:
            print("*get_Captcha_image:", e)
            return 0

    # HTML 가져올 element 의 tag 이름을 설정함
    def set_element_name(self, site, name, nationality, birth_date, gender_male, gender_female,
                         mobile_carrier, mobile_number, captcha_character, agreeInfo):
        if site == self.element_name["사이트"]:  # 기존것과 동일하다면 스킵
            return
        self.element_name["사이트"] = site
        self.element_name["이름"] = name
        self.element_name["국적"] = nationality
        self.element_name["생년월일"] = birth_date
        self.element_name["성별남"] = gender_male
        self.element_name["성별여"] = gender_female
        self.element_name["통신사"] = mobile_carrier
        self.element_name["휴대폰번호"] = mobile_number
        self.element_name["자동입력방지문자"] = captcha_character
        self.element_name["모두동의"] = agreeInfo

    # 사용자 정보 + 자동입력방지문자 입력
    def input_user_info(self, site_name):
        if site_name == "Gmarket":
            print("Gmarket 실행")
            try:
                iframe = self.driver.find_element_by_id("popLayerIframe1")
                self.driver.switch_to.frame(iframe)
            except selenium.common.exceptions.NoSuchElementException as e:
                print("*Error : 입력가능한 Gmarket frame 없음")
                self.successInput = False
                return
            self.set_element_name("Gmarket", "u_name", "naSelect", "birth_date", "gender_male", "gender_female",
                                  "carrier_sel", "cellphone_num", "captchaCode", "agreeInfoAllTop")
        elif site_name == "Auction":
            print("Auction 실행")
            # 옥션은 새창으로 팝업되기때문에 iframe 바꿀 필요 없음
            self.set_element_name("Auction", "name", "naSelect", "ssnLeft8", "sexSelect1", "sexSelect2",
                                  "carrierType", "cpNo", "captchaCode", "agreeInfoAllTop")
        elif site_name == "PASS":
            print("PASS 휴대폰 본인확인 실행")
            # 옥션은 새창으로 팝업되기때문에 iframe 바꿀 필요 없음
            self.set_element_name("PASS", "smsName", "native", "smsBirth", "m_sel", "fm_sel",
                                  None, "smsMobileNum", "s_secureText", None)
            pass
        else:
            print("*Error : 알 수 없는 사이트")
            return

        if self.successInput is False:
            if not self.get_Captcha_image(site_name):
                print("Captcha 이미지 다운로드 실패")
            # user_info["자동입력방지문자"] = OneImageProcessingAndML()     # 이미지로 머신러닝
            self.user_info["자동입력방지문자"] = OneSoundProcessingAndML()       # 사운드로 머신러닝
            print("user_info 입력")

            if not self.input_element(self.element_name["이름"], self.user_info["이름"]):
                print("이름 입력 실패")
                return

            select = Select(self.driver.find_element_by_id(self.element_name["국적"]))
            select.select_by_visible_text(self.user_info["국적"])

            if not self.input_element(self.element_name["생년월일"], self.user_info["생년월일"]):
                print("생년월일 입력 실패")
                return

            if self.element_name["성별남"] is not None and self.element_name["성별여"] is not None:
                try:
                    if self.user_info["성별"] == "남자":
                        self.driver.find_element_by_id(self.element_name["성별남"]).click()
                    else:
                        self.driver.find_element_by_id(self.element_name["성별여"]).click()
                except selenium.common.exceptions.NoSuchElementException:
                    if self.user_info["성별"] == "남자":
                        self.driver.find_element_by_class_name(self.element_name["성별남"]).click()
                    else:
                        self.driver.find_element_by_class_name(self.element_name["성별여"]).click()

            if self.element_name["통신사"] is not None:
                select = Select(self.driver.find_element_by_id(self.element_name["통신사"]))
                select.select_by_visible_text(self.user_info["통신사"])

            if not self.input_element(self.element_name["휴대폰번호"], self.user_info["휴대폰번호"]):
                print("휴대폰 번호 입력 실패")
                return

            if not self.input_element(self.element_name["자동입력방지문자"], self.user_info["자동입력방지문자"]):
                print("자동입력방지문자 입력 실패")
                return
            self.successInput = True

            if self.element_name["모두동의"] is not None:
                self.driver.find_element_by_id(self.element_name["모두동의"]).click()

    # 유저 정보를 설정함
    def set_user_info(self, name, nationality, birth_date, gender, mobile_carrier, mobile_number, string):
        if name:
            self.user_info["이름"] = name
        if nationality:
            self.user_info["국적"] = nationality
        if birth_date:
            self.user_info["생년월일"] = birth_date
        if gender:
            self.user_info["성별"] = gender
        if mobile_carrier:
            self.user_info["통신사"] = mobile_carrier
        if mobile_number:
            self.user_info["휴대폰번호"] = mobile_number

    def do_crawling(self):
        try:
            if self.driver_path == "":
                chrome_driver = "./chromedriver.exe"  # chrome_driver defalut 위치
            else:
                chrome_driver = self.driver_path
            self.driver = webdriver.Chrome(chrome_driver)
            while True:
                try:
                    time.sleep(1)
                    current_url = self.driver.current_url
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    print("-----------------------------------------------------")
                    print("*url : ", self.driver.current_url)
                    print("*successInput :", self.successInput)
                    if "sslmember2.gmarket.co.kr/FindID" in current_url:
                        self.input_user_info("Gmarket")
                    elif "Common/CustomizedVerification" in current_url:
                        self.input_user_info("Auction")
                    elif "mobile-ok.com/SimplePop" in current_url:
                        self.input_user_info("PASS")
                except selenium.common.exceptions.NoSuchWindowException as e:
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    print("*윈도우 바꿈")
                    self.successInput = False
                except selenium.common.exceptions.UnexpectedAlertPresentException as e:
                    print("Unexpected Alert")
                    continue
                except selenium.common.exceptions.WebDriverException as e:
                    print("*크롬 종료 :", e)
                    return
                except BaseException as e:
                    print("*BaseException : ", e)
        except selenium.common.exceptions.WebDriverException as e:
            print("*do 크롬 종료 :", e)
            return
        except BaseException as e:
            print("*Error :", e)
            self.driver.close()
            exit()

