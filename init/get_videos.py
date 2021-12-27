import random
import time
import requests
import json
from faker import Factory
URL = "https://api.bilibili.com/x/space/arc/search?mid={}&pn={}&keyword=阿梓"
URL2 = "https://api.bilibili.com/x/tag/archive/tags?aid={}"
ORDERS = ["totalrank", "click", "pubdate", "dm", "stow"]
TAGS = ["阿梓", "阿梓从小就很可爱"]
PROXIES = [None, "58.53.41.233:7082", "120.196.112.6:3128", "223.16.216.55:8080", "47.103.30.89:8080", "27.191.60.226:8089", "120.25.232.56:59394", "27.191.60.51:8089", "139.217.101.53:9080", "101.132.136.155:8080", "106.14.43.211:8080", "47.94.100.76:3128", "18.166.177.241:10809"]
factory = Factory.create()
proxy = None
aids = []

def process(author, page):
    global proxy
    global aids
    while True:
        try:
            print(f"{author} {page}（代理:{proxy}）")
            videos = requests.get(URL.format(author, page), headers={'User-Agent': factory.user_agent()}, proxies=proxy, timeout=2).json()["data"]["list"]["vlist"]
            if len(videos) == 0:
                return False
            for video in videos:
                aid = video["aid"]
                if author == 7706705:
                    aids.append(aid)
                    continue
                tags = requests.get(URL2.format(aid), headers={'User-Agent': factory.user_agent()}, proxies=proxy, timeout=2).json()["data"]
                ok = False
                for tag in tags:
                    if tag["tag_name"] in TAGS:
                        ok = True
                        break
                if ok:
                    aids.append(aid)
            return True
        except Exception as e:
            print(f"错误，重试（信息：{e}）")
            proxy = {"https": random.choice(PROXIES)}

with open("authors.json") as fp:
    authors = json.load(fp)
for author in authors:
    page = 1
    while process(author, page):
        page += 1
        time.sleep(0.03)
    with open("videos.json", "a") as fp:
        for aid in aids:
            print(aid, file = fp, end = ',')
        aids = []