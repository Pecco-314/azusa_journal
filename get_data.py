import asyncio
import functools
import requests
import json
import random
import datetime
from colorama import Fore
import sys
from faker import Factory

URL = "https://api.bilibili.com/archive_stat/stat?aid={}"
factory = Factory.create()
result_map = {}

def get_proxy():
    return requests.get("http://localhost:5010/get").json().get('proxy')

async def crawler(aid):
    global result_map
    proxy = {"https": get_proxy()}
    while True:
        try:
            # print(f"{aid} {proxy['https']}")
            url = URL.format(aid)
            future = asyncio.get_event_loop().run_in_executor(None, functools.partial(requests.get,
                url,
                # headers = {'User-Agent': factory.user_agent()},
                timeout=2, 
                proxies=proxy
            ))
            response = await future
            obj = response.json()
            if obj['code'] == 40003: # 已删除的视频
                return
            data = obj['data']
            result_map[aid] = {
                "view": data["view"],
                "favorite": data["favorite"],
                "coin": data["coin"],
                "like": data["like"]
            }
            break
        except Exception:
            proxy = {"https": get_proxy()}

    print(f"已完成{len(result_map)}/{len(aids)}")
    if len(result_map) % 100 == 0:
        with open(f"log/{sys.argv[1]}.txt", "a") as fp:
            fp.write(f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] {len(result_map)}/{len(aids)}\n")
            fp.flush()
    

if __name__ == '__main__':
    with open(f"log/{sys.argv[1]}.txt", "w"):
        pass
    start = datetime.datetime.now()
    with open("videos.json") as fp:
        aids = json.load(fp)['list']
    loop = asyncio.get_event_loop()
    tasks = [crawler(aid) for aid in aids]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    with open(f"data/{sys.argv[1]}.json", "w") as fp:
        json.dump(result_map, fp)
    end = datetime.datetime.now()
    print(f"已全部完成（{(end - start).total_seconds()}秒）")
