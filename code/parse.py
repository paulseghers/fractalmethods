import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

import shapefile
from svgpathtools import svg2paths

def read_shp(fname):
    sf = shapefile.Reader(fname)

    l = []
    for s in sf.shapes():
        if s.shapeType not in (3,5):
            raise ValueError('not a polygon / polyline')
        s.parts.append(len(s.points))
        for li,ri in zip(s.parts,s.parts[1:]): # each part is a polyline
            l.append(np.array(s.points[li:ri]))
    return l # list of curves

def read_svg(fname):
    paths, attr = svg2paths(fname)
    l = []
    for p in paths:
        x = np.array([ c.start for c in p ] + [ p[-1].end ])
        l.append(np.c_[x.real,x.imag]) # was stored as complex number
    return l # list of curves

def pick(l, x,y):
    # indices of things intersecting with x,y
    # make bounding boxes
    bb = np.array([(*x.min(axis=0),*x.max(axis=0)) for x in l])
    return np.where((bb[:,0]<x) & (bb[:,2]>x) & (bb[:,1]<y) & (bb[:,3]>y))[0]

def expand(l):
    # list of curves to segments
    res = []
    for c in l:
        res += list( np.c_[c[:-1],c[1:]].reshape(-1,2) )
    return np.array(res)

def only_coast(l, bmp):
    # list of segment, return only ones which are on the coast
    # bitmap corresponding to svg, 1 if inside, 0 if outside
    rot = np.array([[0,1],[1,0]])
    res = []
    for i in range(0,len(l),2):
        a,b = l[i:i+2]
        m = (a+b) / 2
        d = rot @ (b-a) / 2
        i1,j1 = m+d
        i2,j2 = m-d
        if bmp[int(j1),int(i1)] + bmp[int(j2),int(i2)] < 2:
            res.append(a)
            res.append(b)
    return np.array(res)



if __name__ == '__main__':
    if False: # GB
        l = read_shp('data/TM_WORLD_BORDERS-0.3.shp')
        # Great Britain index
        GBi = pick(l,-2,53)[0] # 3063
        GB = l[GBi]
        print(f'GB index: {GBi}, shape: {GB.shape}')
        fig,ax = plt.subplots()
        ax.plot(*GB.T)
        ax.set_aspect(1)
        plt.show()
    else: # norway
        l = expand(read_svg('data/norge.svg'))
        bmp = (np.array(Image.open('data/norge.png'))[:,:,0] > 0).astype(int)
        coast = only_coast(l, bmp)
        print(f'original:{len(l)}\n'
              f'   coast:{len(coast)}')