import sys
import random
randomi = random.randint(90,110)
count = 0
for line in sys.stdin:
    try:
        l = line.strip().split()
        u=""
        i=""
        if len(l)==3:
            u,i,t=l
        elif len(l)==4:
            u,i,t,tt=l
        elif len(l) == 1:
            try:
                l = l[0].split("\x01")
                u = l[0]
                x = l[1]
                ll = x.split("|")
                if len(ll) > 1:
                    for item in ll:
                        if count == randomi:
                            print(item + "\t" + u + "\t" + str(-1))
                            count = 0
                            randomi = random.randint(900,1100)
                        count += 1
                continue
            except:
                continue
        else:
            i,u,t=l[0].split("\x01")
        if len(u)>3 and len(i)>3 and len(i.split())<2 and len(u.strip().split())<2:
            t = int(t)
            if t>1000:
                t = int(t/1000)
            print i+"\t"+u+"\t"+str(t)

    except:
        continue
