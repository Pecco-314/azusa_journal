import sys
import json
d1 = sys.argv[1]
d2 = sys.argv[2]
with open(f"data/{d1}.json") as fp:
    map1 = json.load(fp)
with open(f"data/{d2}.json") as fp:
    map2 = json.load(fp)
for k, v in map2.items():
    info = map1.get(k, {'view':0, 'coin':0, 'like':0, 'favorite':0})
    v['view'] -= info['view']
    v['coin'] -= info['coin']
    v['like'] -= info['like']
    v['favorite'] -= info['favorite']
with open(f"data/delta_{d1}_{d2}.json", 'w') as fp:
    json.dump(map2, fp)