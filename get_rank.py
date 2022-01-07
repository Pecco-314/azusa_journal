import json
import requests
import sys

URL = "http://api.bilibili.com/x/web-interface/view?aid={}"

def get_point(view, coin, favorite, like):
    if view == 0:
        return 0
    A = coin * 2 + favorite * 2 + like
    return A * min(0.5, A / view) * 200 + view

map = json.load(open(f"data/{sys.argv[1]}.json"))
videos = []
for k, v in map.items():
    videos.append({
        'aid': k,
        'view': v['view'],
        'coin': v['coin'],
        'favorite': v['favorite'],
        'like': v['like'],
        'point': get_point(v['view'], v['coin'], v['favorite'], v['like'])
    })
videos.sort(key=lambda k : -k['point'])
exclusive = json.load(open("exclusive.json"))
rk = 0
for video in videos:
    if video['aid'] in exclusive:
        continue
    obj = requests.get(URL.format(video['aid'])).json()
    if obj['code'] != 0:
        continue
    rk += 1
    data = obj['data']
    print(f"""第{rk}名：{data['title']}（av{data['aid']}）
    作者：{data['owner']['name']}
    点数：{video['point']}
    播放量：{video['view']}
    硬币：{video['coin']}
    收藏：{video['favorite']}
    点赞：{video['like']}
    """)
    if rk == 25:
        break
