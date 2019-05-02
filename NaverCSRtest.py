import sys
import os
import requests
client_id = "lwig6v5ajr"
client_secret = "fF27nrpFLo1kuFsKJz0jGXuV8xS1zTwqLc24w7gB"
lang = "Eng" # 언어 코드 ( Kor, Jpn, Eng, Chn )

path_dir = "./listen_test/"
file_list = os.listdir(path_dir)
file_list.sort()

alpha = {
    "A": [],
    "B": [],
    "C": [],
    "D": [],
    "E": [],
    "F": [],
    "G": [],
    "H": [],
    "I": [],
    "J": [],
    "K": [],
    "L": [],
    "M": [],
    "N": [],
    "O": [],
    "P": [],
    "Q": [],
    "R": [],
    "S": [],
    "T": [],
    "U": [],
    "V": [],
    "W": [],
    "X": [],
    "Y": [],
    "Z": [],
}
url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang

headers = {
    "X-NCP-APIGW-API-KEY-ID": client_id,
    "X-NCP-APIGW-API-KEY": client_secret,
    "Content-Type": "application/octet-stream"
}

for file_name in file_list:
    data = open(path_dir + file_name, 'rb')
    response = requests.post(url, data=data, headers=headers)
    rescode = response.status_code
    if rescode == 200:
        myDict = eval(response.text)
        myString = myDict["text"].upper()
        myList = myString.split(" ")
        print(file_name, myList)
        # if len(myList) == 5:
        #     print(myList)
        #     for i in range(5):
        #         if not myList[i] in file_name[i]:
        #             alpha[file_name[i]].append(myList[i])
    else:
        print("Error : " + response.text)


for i in alpha:
    print(i, " : ", alpha[i])
