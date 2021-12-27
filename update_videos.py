import requests
import json
from faker import Factory

URL = 'https://api.bilibili.com/x/web-interface/search/type?page={}&order=pubdate&keyword=阿梓&search_type=video'
URL2 = 'https://api.bilibili.com/x/space/arc/search?mid=7706705&page={}'


def get_proxy():
    return {"https": requests.get("http://localhost:5010/get").json().get('proxy')}

def change_proxy():
    global proxy
    proxy = get_proxy()

def try_until_succeed(func, handler, log = False):
    while True:
        try:
            return func()
        except Exception as e:
            handler()
            if log:
                print(e)

with open("videos.json") as fp:
    result = json.load(fp)
timestamp = result['timestamp']
factory = Factory.create()
page = 1
lst = result['list']
cnt = 0
latest = 0
breakall = False
proxy = None
while True:
    response = try_until_succeed(lambda: requests.get(URL.format(page), timeout=2, headers = {'User-Agent': factory.user_agent()}, proxies=proxy), change_proxy, True).json()
    for video in response['data']['result']:
        if video['pubdate'] < timestamp:
            breakall = True
            break
        latest = max(latest, video['pubdate'])
        tags = video['tag'].split(',')
        if '阿梓' in tags or '阿梓从小就很可爱' in tags:
            lst.append(video['aid'])
            cnt += 1
    if breakall:
        break
    page += 1
page = 1
while True:
    response = try_until_succeed(lambda: requests.get(URL2.format(page), timeout=2, headers = {'User-Agent': factory.user_agent()}, proxies=proxy), change_proxy, True).json()
    for video in response['data']['list']['vlist']:
        if video['created'] < timestamp:
            breakall = True
            break
        latest = max(latest, video['created'])
        lst.append(video['aid'])
        cnt += 1
    if breakall:
        break
    page += 1
with open("videos.json", 'w') as fp:
    result = json.dump({'timestamp':latest, 'list':list(set(lst))}, fp)
print(f"已更新{cnt}个视频")