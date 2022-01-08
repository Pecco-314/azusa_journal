import os
import datetime

now = datetime.datetime.now()
t = f"{now:%Y-%m-%d}"
t2 = f"{now - datetime.timedelta(7):%Y-%m-%d}"
t3 = f"{now - datetime.timedelta(14):%Y-%m-%d}"
os.system("python3 update_videos.py")
os.system(f"python3 get_data.py {t}")
if now.weekday() == 1:
    os.system(f"python3 get_delta.py {t2} {t}")
    os.system(f"python3 get_rank.py delta_{t2}_{t} delta_{t3}_{t2} > data/rank_{t2}_{t}.txt")
