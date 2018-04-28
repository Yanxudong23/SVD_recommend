import sys
pre=None
u_set=set()
min_view=int(sys.argv[1])
for line in sys.stdin:
    i,u,t=line.strip().split()
    u = u +":"+str(t)
    if i==pre:
        u_set.add(u)
    else:
        if pre!=None and len(u_set) >=min_view:
            print pre+"\t"+",".join(u_set)
        u_set=set()
        u_set.add(u)
        pre=i
if pre!=None and len(u_set)>=min_view:
    print i+"\t"+",".join(u_set)
