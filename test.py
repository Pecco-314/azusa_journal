import requests
def get_proxy():
    return requests.get("http://localhost:5010/get?type=https").json().get('proxy')

print(requests.get('https://api.bilibili.com/archive_stat/stat?aid=716386834', proxies = {"https" : get_proxy()}, timeout=3).json())