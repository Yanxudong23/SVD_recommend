import sys
import math
import traceback
import collections

for line in sys.stdin:
    try:
        l = line.strip().split()
        if len(l) != 2:
            continue
        i,ul = line.strip().split()
        u = ul.split(",")
        length = len(u)
        dic = {}
        for num in u:
            t = num.split(":")
            user = t[0]
            time = int(t[1])
            if time == -1:
                print(user + "\t" + i + "\t" + str(0))
                continue
            dic.setdefault(user, time)
        kd = collections.OrderedDict(sorted(dic.items(), key=lambda t: t[1], reverse=True))
        count = 0
        for key1, value1 in kd.items():
            if count <= int(length/5):
                print(key1 + "\t" + i + "\t" + str(5))
            elif count <= int(length/5 * 2):
                print (key1 + "\t" + i + "\t" + str(4))
            elif count <= int(length/5 * 3):
                print (key1 + "\t" + i + "\t" + str(3))
            elif count <= int(length/5 * 4):
                print (key1 + "\t" + i + "\t" + str(2))
            else:
                print (key1 + "\t" + i + "\t" + str(1))
            count += 1

    except:
        traceback.print_exc()
        continue