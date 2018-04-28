import sys
import traceback

min_clk = sys.argv[1]
pre = None
item = set()

for line in sys.stdin:

    ll = line.strip().split()
    if len(ll) != 3:
        continue
    u = ll[0]
    i = ll[1] + ":" + str(ll[2])
    if u == pre:
        item.add(i)
    else:
        if pre != None and len(item) >= int(min_clk):
            print (pre+"\t"+",".join(item))
        item = set()
        item.add(i)
        pre = u

if pre != None and len(item) >= int(min_clk):
    print (pre + "\t" + ",".join(item))
