# -*- coding: utf8 -*-

import requests
import random
import time
import sched
import json

# 配置信息
phone = "18679500353"    # 手机号
password = "txt245780"  #密码
desc = "我在这里"   #签到文本
longitude = "116.404267"  #经度
latitude = "39.910131"   #纬度
address = "九江112"   #签到地点名
stateType = "START 21.20 END21.23"  #START 上班 END 下班
sec = 800  # 延迟签到的上限时间，单位为秒
# 配置信息

loginUrl = "https://api.moguding.net:9000/session/user/v1/login"
saveUrl = "https://api.moguding.net:9000/attendence/clock/v1/save"
planUrl = "https://api.moguding.net:9000/practice/plan/v1/getPlanByStu"

inc = random.randint(0,sec)
schedule = sched.scheduler(time.time, time.sleep)

def getToken():
    data = {
        "password": password,
        "loginType":"android",
        "uuid":"",
        "phone": phone
    }

    resp = postUrl(loginUrl,data=data, headers={"Content-Type": "application/json; charset=UTF-8",'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36'})
    return resp['data']['token']

def getPlanId(headers):
    data = {"state":""}
    resp = postUrl(planUrl,headers,data)
    return resp['data'][0]['planId']

def main():
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36',
        'roleKey': 'student',
        'Authorization': getToken()
    }

    data = {
        'device': 'Android',
        'address': address,
        'description': desc,
        'country': '',
        'province': '',
        'city': '',
        'longitude': longitude,
        'latitude': latitude,
        'planId': getPlanId(headers),
        'type': stateType
    }
    resp = postUrl(saveUrl,headers,data)
    print(resp)

def postUrl(url,headers,data):
    requests.packages.urllib3.disable_warnings()
    resp = requests.post(url, headers=headers, data=json.dumps(data),verify=False)
    return resp.json()

def main_handler(event, context):
    print("延迟%s秒签到" % inc)
    
    schedule.enter(inc, 0, main, ())
    schedule.run()

    print("在%s签到成功！" % address)
    return("happy~")
