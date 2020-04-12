# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 22:42:14 2020

@author: Zpaffled
"""

from dim import bcnt
from fracgen import sierpinsky
from time import time
import numpy as np

import matplotlib.pyplot as ptl


def intersect(seg,x,y):
    # in sierpinsk x1!=x2
    (x1,y1),(x2,y2) = seg
    if min(x1,x2)>x or max(x1,x2)<x+1 \
    or min(y1,y2)>y or max(y1,y2)<y+1:
        return False
    d = (y2-y1) / (x2-x1)
    o = x1/y1
    Y1 = x*d + o
    Y2 = (x+1)*d + o
    return min(Y1,Y2)<y+1 and max(Y1,Y2)>y

def bcnt_naive(f, res):
    f = f/ res
    xl,yl,xh,yh = (int(x) for x in (*f.min(axis=0),*f.max(axis=0)))
    cnt = 0
    for x in range(xl,xh+1):
        for y in range(yl,yh+1):
            for i in range(0,len(f),2):
                if intersect(f[i:i+2],x,y):
                    cnt += 1
                    break
    return cnt

res = np.logspace(-5,-2,num=4,base=2,)

fig,ax = plt.subplots(figsize=(8,6))
for depth in [3, 4, 5,]:
    f = sierpinsky(depth)
    
    tl = []
    for r in res:
        t0 = time()
        for _ in range(3):
            bcnt(f, r, coast=False)
        t1 = time()
        tl.append((t1-t0)/3)
    plt.loglog(res,tl,label=f'improved, depth:{depth}',marker='x')
    
    tl = []
    for r in res:
        t0 = time()
        bcnt_naive(f, r)
        t1 = time()
        tl.append(t1-t0)
    plt.loglog(res,tl,label=f'naive, depth:{depth}',marker='x')
    print('peps')

plt.xlabel('delta')
plt.ylabel('time (in s)')
plt.legend()
plt.show()
    
    