from fracgen import *
from dim import *
import matplotlib.pyplot as plt
fig,ax = plt.subplots(3,2)

def subplti(i):
    if i == 0 or i == 1: 
        return 0
    if i == 2 or i == 3:
        return 1
    else:
        return 2

deltas = np.logspace(-7, -2, num=40, base=2)
name = "vonkoch_6_depths"
for i,d in enumerate([1,3,4,7,8,9]):#,8,9
    f = vonkoch(d)
    results = [
        np.mean( [ bcnt(f + delta * np.random.rand(2), delta, coast=True) #False for sierpinski, true for vonkoch
            for _ in range(5) ] )
        for delta in deltas ]
    s,o = np.polyfit(np.log(deltas), np.log(results), 1)
    a, b = subplti(i), i%2
    ax[a,b].loglog(deltas,np.exp(s*np.log(deltas)+o),label='trend', color="orange")
    ax[a,b].scatter(deltas, results, marker='.',label='computed pts')
    ax[a,b].set_title(f'depth={d} - dim={-s:.3}')
    #ax[a,b].legend()
    #plt.title("Different values of the Box-counting dimension of the sierpinski triangle for different recusrion depths")
    plt.subplots_adjust(hspace=0.8, wspace=0.4)
    #plt.tight_layout()
    plt.savefig(name+'.png',format="png", dpi=300, bbox_inches="tight", pad_inches=0)
#plt.show()

