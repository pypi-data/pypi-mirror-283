# -*- coding: UTF-8 -*-
# python3

import requests
from devolib.util_log import LOG_D, LOG_E

# 关闭证书校验
# import requests,warnings
# from requests.packages import urllib3
# # 关闭警告
# urllib3.disable_warnings()
# warnings.filterwarnings("ignore")
# 1，关闭证书
# res = requests.get(url="https://www.12306.cn",verify=False)  #不验证证书,报警告,返回200
# print(res.content.decode("utf-8"))

def GET(host, path):
    url = f'{host}{path}'
    LOG_D(f'GET REQ: {url}')

    response = requests.get(url)
    if response.status_code == 200:
        LOG_D(f'GET RES: {response.text}')
        return response.text
    else:
        LOG_E(f'GET ERR: {response.status_code}')
        return None

def POST(host, path, data, headers={}):
    # 定义自定义 header
    internal_headers = {
        'User-Agent': 'My Custom User Agent',
        'Content-Type': 'application/json',  # 假设发送 JSON 数据
    }

    headers.update(internal_headers)

    # 发送 POST 请求
    url = f'{host}{path}'
    LOG_D(f'POST REQ: {url}, {headers}, {data}')

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        LOG_D(f'POST RES: {response.text}')
        return response.text
    else:
        LOG_E(f'POST ERR: {response.status_code}')
        return None

'''
@brief Http for client
'''
class Httpc:
    pass