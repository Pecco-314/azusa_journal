import os
import datetime

now = datetime.datetime.now()
t = f"{now:%Y-%m-%d}"
t2 = f"{now - datetime.timedelta(7):%Y-%m-%d}"
os.system("python3 update_videos.py")
os.system(f"python3 get_data.py {t}")
# if now.weekday() == 1:
#     os.system("python3 get_delta.py {t2} {t}")
#     os.system("python3 get_rank.py delta_{t2}_{t} > data/rank_{t2}_{t}")
