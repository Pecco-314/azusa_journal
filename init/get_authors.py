import random
import time
import requests
from faker import Factory
URL = "https://api.bilibili.com/x/web-interface/search/type?page={}&order=pubdate&keyword={}&search_type=video&order={}"
ORDERS = ["totalrank", "click", "pubdate", "dm", "stow"]
TAGS = ["阿梓", "阿梓从小就很可爱"]
PROXIES = [None, "58.53.41.233:7082", "120.196.112.6:3128", "223.16.216.55:8080", "47.103.30.89:8080", "27.191.60.226:8089", "120.25.232.56:59394", "27.191.60.51:8089", "139.217.101.53:9080", "101.132.136.155:8080", "106.14.43.211:8080", "47.94.100.76:3128", "18.166.177.241:10809"]
factory = Factory.create()
proxy = None
with open("authors.json", "a") as fp:
    for tag in TAGS:
        for order in ORDERS:
            for p in range(1, 51):
                while True:
                    print(f"processing {tag} {order} {p}（代理：{proxy}）")
                    try:
                        response = requests.get(URL.format(p, tag, order), headers = {'User-Agent': factory.user_agent()}, proxies=proxy, timeout=3)
                        if (response.status_code != 200):
                            raise Exception(response.status_code)
                        for video in response.json()['data']['result']:
                            print(video["mid"], file = fp, end=",")
                        time.sleep(0.03)
                        break
                    except Exception as e:
                        print(f"错误，5秒后重试（信息：{e}）")
                        proxy = {"https": random.choice(PROXIES)}
                        time.sleep(5)
