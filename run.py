import os
import datetime

now = datetime.datetime.now()
t = f"{now:%Y-%m-%d}"
t2 = f"{now - datetime.timedelta(7):%Y-%m-%d}"
os.system("python update_videos.py")
os.system(f"python get_data.py {t}")
# if t.weekday() == 0:
#     os.system("python get_delta.py {t} {t2}")
#     os.system("python get_rank.py delta_{t}_{t2}")