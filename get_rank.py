import json
import requests
import sys

URL = "http://api.bilibili.com/x/web-interface/view?aid={}"

def get_point(view, coin, favorite, like):
    if view == 0:
        return 0
    A = coin * 2 + favorite * 2 + like
    return A * min(0.5, A / view) * 200 + view

this = json.load(open(f"data/{sys.argv[1]}.json"))
last = {}
if len(sys.argv) >= 3:
    last = json.load(open(f"data/{sys.argv[2]}.json"))
exclusive = json.load(open("exclusive.json"))

def get_video_list(map):
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
    return videos

this_videos = get_video_list(this)
last_videos = get_video_list(last)
for video in last_videos:
    if video.get('rank') is not None:
        this_videos['rank'] = '-'

def get_change(last, this):
    if last is None:
        return 'New'
    elif last == '-':
        return 'Re'
    elif last == this:
        return '--'
    elif last < this:
        return f'↓{this - last}'
    else:
        return f'↑{last - this}'

rk = 0
for video in this_videos:
    if video['aid'] in exclusive:
        continue
    obj = requests.get(URL.format(video['aid'])).json()
    if obj['code'] != 0:
        continue
    rk += 1
    data = obj['data']
    last_video = last.get(video['aid'])
    last_rank = None if last_video is None else last_video.get('rank')
    print(f"""第{rk}名（{get_change(last_rank, rk)}）：{data['title']}（av{video['aid']}）
    作者：{data['owner']['name']}
    点数：{video['point']}
    播放量：{video['view']}
    硬币：{video['coin']}
    收藏：{video['favorite']}
    点赞：{video['like']}
    """)
    this[video['aid']]['rank'] = rk
    if rk == 25:
        break

with open(f"data/{sys.argv[1]}.json", "w", encoding='utf-8') as fp:
    json.dump(this, fp)