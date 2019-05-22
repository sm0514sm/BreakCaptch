import requests


def aaa(url, referer):
    cookie = 'pcid=1558356403914; cguid=11558356403737005811000000; sguid=31558356403737005811274000; pguid=21558356403737005811010000; WMONID=P_D_sREpAj2; RPM=BT%3DL1558356410365; AGP=fccode=AH41; channelcode=0C42; ssguid=315585000520530047312740000; gen=1KRgroBk1H45VAtrQ0OlmeMHzynS41CcSzdnr8/0NuK5d/d556P5lMX4OjtRumv2AZID/DSU5M/zX+/xQUIxB7pPGqceA1rBRT3eoAB16fY='

    print(cookie)

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