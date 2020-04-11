import numpy as np
import matplotlib.pyplot as plt

def vonkoch(depth):
    rot = np.array([[0,-1],[1,0]])
    pts = np.array([[0,0],[1,0]])
    for _ in range(depth):
        l,r = pts[:-1],pts[1:]
        # mid pts
        m1 = l*2/3 + r/3
        m3 = l/3 + r*2/3
        m2 = (l/2 + r/2 + (rot @ (m3-m1).T * np.sqrt(3)/2).T)
        # concatenate
        pts = np.c_[l,m1,m2,m3].reshape(-1,2)
        pts = np.r_[pts,[[1,0]]]
    return pts # as coast

def sierpinsky(depth):
    T = np.array([[0,0],[1,0],[1/2,np.sqrt(3)/2]])
    T -= np.mean(T,axis=0)
    a,b,c = T/2
    for i in range(depth):
        T /= 2
        T = np.concatenate([T+a,T+b,T+c])
    # dark triangle magic
    f = np.array(T).reshape(-1,3,2) # 0,1,2
    f = np.r_['1',f,f].reshape(-1,2) # 0,1 2,0 1,2
    return f # as segments

if __name__ == '__main__':
    F = vonkoch(10)
    # F = sierpinsky(10)
    fig,ax = plt.subplots()
    ax.plot(*F.T)
    ax.set_aspect(1)
    plt.show()

