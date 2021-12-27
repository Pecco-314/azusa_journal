import requests
import json

URL = 'https://api.bilibili.com/x/web-interface/search/type?page={}&order=pubdate&keyword=阿梓&search_type=video'

page = 1
with open("videos.json") as fp:
    result = json.load(fp)
timestamp = result['timestamp']
lst = result['list']
cnt = 0
latest = -1
breakall = False
while True:
    response = requests.get(URL.format(page)).json()
    for video in response['data']['result']:
        if video['pubdate'] < timestamp:
            breakall = True
            break
        if latest == -1:
            latest = video['pubdate']
        tags = video['tag'].split(',')
        if '阿梓' in tags or '阿梓从小就很可爱' in tags:
            lst.append(video['aid'])
            cnt += 1
    if breakall:
        break
    page += 1
with open("videos.json", 'w') as fp:
    result = json.dump({'timestamp':latest, 'list':list(set(lst))}, fp)
print(f"已更新{cnt}个视频")