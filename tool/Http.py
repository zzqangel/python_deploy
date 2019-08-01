#!/usr/bin/python3
# coding:utf-8
import requests


def http_request_ret_content(url):
    r0 = requests.get(url)
    if not r0.status_code == 200:
        raise RuntimeError("http connection fail with code {0}".format(r0.status_code))
    content = str(r0.content).strip()
    if content.startswith("b\'") and content.endswith("\'"):
        content = content['b\''.__len__():content.__len__() - 1]
    return content


def http_request_post_ret_content(url, data=None, json=None):
    headers = {'content-type': "application/json"}
    r0 = requests.post(url, data=data, json=json, headers=headers)
    if not r0.status_code == 200:
        raise RuntimeError("http connection fail with code {0}".format(r0.status_code))
    content = str(r0.content).strip()
    print(content)
    if content.startswith("b\'") and content.endswith("\'"):
        content = content['b\''.__len__():content.__len__() - 1]
    return content


def http_request_ret_200(url):
    r0 = requests.get(url)
    return r0.status_code == 200

# print(http_request_ret_content(
#     "http://172.31.15.10:8500/v1/agent/health/service/name/{}?format=text".replace("{}", "id-creator-service")))
