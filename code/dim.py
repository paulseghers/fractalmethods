import numpy as np
import matplotlib.pyplot as plt

def bcnt(f,res,coast=True):
    # fractal, resolution, coast or list of segments
    n = len(f)
    s = set()
    f = f/res # dont modify f
    rng = range(n-1) if coast else range(0,n,2)
    for i in rng: # coast
        dx,dy = f[i+1]-f[i]
        if dx*dy >= 0: # going /
            if dx+dy > 0: # normal
                a,b = f[i],f[i+1]
                dx,dy = -dy,dx
            else: # reverse
                a,b = f[i+1],f[i]
                dx,dy = dy,-dx
            o = a[0]*dx + a[1]*dy
            # going up right
            x,y = a.astype(int) # start sq
            s.add((x,y))
            bx,by = b.astype(int) # end sq
            while x<bx or y<by:
                if (x+1)*dx + (y+1)*dy > o: x += 1 # point above go right
                else: y += 1 # point below go up
                s.add((x,y))
        else: # going \
            if dx-dy > 0: # normal
                a,b = f[i],f[i+1]
                dx,dy = -dy,dx
            else: # reverse
                a,b = f[i+1],f[i]
                dx,dy = dy,-dx
            o = a[0]*dx + a[1]*dy
            # going up right
            x,y = a.astype(int) # start sq
            s.add((x,y))
            bx,by = b.astype(int) # end sq
            while x<bx or y>by:
                if (x+1)*dx + (y-1)*dy < o: x += 1 # point below go right
                else: y -= 1 # point above go down
                s.add((x,y))
    # can scatter np.array(list(s))
    return len(s)

def dcnt(f,d,coast=True):
    if not coast:
        raise ValueError('divider prefers coasts')

    rot = np.array([[0,-1],[1,0]])
    def c1_line(c,p1,p2):
        d = p2-p1
        d /= np.linalg.norm(d)
        a = (rot @ d) @ (p1-c)
        return c + a*(rot@d) + np.sqrt(1.-a*a)*d

    n = len(f)-1
    f = f/d
    c = f[0]
    cnt = 1
    ans = [c]
    for i in range(n):
        while True:
            d = f[i+1]-c
            if d@d < 1: break
            cnt += 1
            c = c1_line(c,f[i],f[i+1])
            ans.append(c)
    # can plot ans
    return len(np.array(ans))

def dim(f, method='box', coast=True, scale=None, smooth=5):
    if scale is None:
        sz = min(np.max(f,axis=0)-np.min(f,axis=0))
        sz = np.log2(sz)
        scale = sz-7, sz-2
    deltas = np.logspace(scale[0], scale[1], num=50, base= 2)
    cnt = {'div':dcnt, 'box':bcnt}[method]
    if method == 'div':
        smooth = 1 # 1 = no offset, any other number means we will compute with n random offsets 
    results = [
        np.mean( [ cnt(f + delta * np.random.rand(2), delta, coast=coast)
            for _ in range(smooth) ] )
        for delta in deltas ]
    s,i = np.polyfit(np.log(deltas), np.log(results), 1)
    print(f'Nmax:{results[0]}\nNmin:{results[-1]}\nHdim: {-s:.5}')
    plt.scatter(deltas, results, marker='.',label='pts')
    plt.loglog(deltas,np.exp(s*np.log(deltas)+i),label='trend')
    plt.title(f'{method} dim {-s:.3}')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    from fracgen import vonkoch
    #f = vonkoch(9)
    f = get_isle()
    dim(f, 'div')
