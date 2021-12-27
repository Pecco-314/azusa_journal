import json
import os
filename = "videos.json"
lst = json.load(open(filename))
lst = list(set(lst))
json.dump(lst, open("tmp", "w"))
os.system(f"powershell -c rm {filename}")
os.system(f"powershell -c ren tmp {filename}")