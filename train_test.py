import sys
import numpy as np
import scipy as sp
from numpy.random import random
try:
    import cPickle as pickle
except ImportError:
    import pickle
import collections

#data = open(sys.argv[1])
para = int(sys.argv[1])

List = []
bi = {}
bu = {}
qi = {}
pu = {}
movie_user = {}
user_movie = {}
# ave = 0
movie = set()


def train(steps=20, gamma=0.04, Lambda=0.15):
    for step in range(steps):
        print 'the ', step, '-th  step is running'
        rmse_sum = 0.0
        kk = np.random.permutation(X.shape[0])
        for j in range(X.shape[0]):

            i = kk[j]
            uid = X[i][0]
            oid = X[i][1]
            rat = int(X[i][2])
            eui = rat - pred(uid, oid)
            rmse_sum += eui ** 2
            bu[uid] += gamma * (eui - Lambda * bu[uid])
            bi[oid] += gamma * (eui - Lambda * bi[oid])
            temp = qi[oid]
            qi[oid] += gamma * (eui * pu[uid] - Lambda * qi[oid])
            pu[uid] += gamma * (eui * temp - Lambda * pu[uid])
            #print(pu)
        gamma = gamma * 0.93
        print "the rmse of this step on train data is ", np.sqrt(rmse_sum / count)
    print(pu)
    # self.test(test_data)


def pred(uid, oid):
    bi.setdefault(oid, 0)
    bu.setdefault(uid, 0)
    qi.setdefault(oid, np.zeros((para, 1)))
    pu.setdefault(uid, np.zeros((para, 1)))
    #if qi[oid] == None:
     #   qi[oid] = np.zeros((para, 1))
    #if (pu[uid] == None):
    #    pu[uid] = np.zeros((para, 1))
    ans = bi[oid] + bu[uid] + np.sum(qi[oid] * pu[uid])
    #print(ans)
    '''
    if ans > 5:
        return 5
    elif ans < 1:
        return 1
       '''
    return ans


def test():
    #f = open('test.txt', 'rb')
    #p = pickle.load(f)
    length = len(bu)
    count = 0
    f1 = open('data.txt', 'w')
    for user in bu.keys():
        d = {}
        for kk in movie:
            if kk in user_movie[user].keys():
                continue
            rank = pred(user, kk)
            d.setdefault(kk, rank)
        kd = collections.OrderedDict(sorted(d.items(), key=lambda t: t[1],reverse=True)[:20])
        it = []
        for key1, value1 in kd.items():
            Str = str(key1) + ":" + str(value1)
            it.append(Str)
        watch = user_movie[user]
        W = []
        dd = {}
        for w in watch:
            dd.setdefault(w, int(user_movie[user][w]))
        kdd = collections.OrderedDict(sorted(dd.items(), key=lambda t: t[1], reverse=True)[:50])
        for key2, value2 in kdd.items():
            Str = str(key2) + ":" + str(value2)
            W.append(Str)
        f1.write(user + "\t" + ",".join(W) + "\t" + "Not watching" + "\t" + ",".join(it) + "\n")

        if count % 1000 == 0:
            print(str(count) + "/" + str(length))

        count += 1

    #f.close()
    f1.close()


#f = data.readlines()
count = 0

for line in sys.stdin:

    ll = line.strip().split()
    if len(ll) != 2:
        continue
    uid = ll[0]
    item = ll[1].split(",")
    for i in item:
        i = i.split(":")
        oid = i[0]
        rat = int(i[1])
        lis = [uid, oid, i[1]]
        List.append(lis)

        movie_user.setdefault(oid, {})
        user_movie.setdefault(uid, {})
        movie_user[oid][uid] = rat
        user_movie[uid][oid] = rat

        movie.add(oid)
        bi.setdefault(oid, 0)
        bu.setdefault(uid, 0)
        qi.setdefault(oid, random((para, 1)) / 10 * (np.sqrt(para)))
        pu.setdefault(uid, random((para, 1)) / 10 * (np.sqrt(para)))
        # ave += rat

        if count % 10000 == 0:
            print(count)
        count += 1

X = np.array(List)
# ave = ave/count
print(count)
print "train start"
train()
print("test start")
test()
print("test success")

