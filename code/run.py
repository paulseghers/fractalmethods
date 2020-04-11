from parse import *
from fracgen import *
from dim import dim

def get_GB():
    l = read_shp('data/TM_WORLD_BORDERS-0.3.shp')
    # Great Britain index
    GBi = pick(l,-2,53)[0] # 3063
    return l[GBi]

def get_norwae():
    l = expand(read_svg('data/norge.svg'))
    bmp = (np.array(Image.open('data/norge.png'))[:,:,0] > 0).astype(int)
    return only_coast(l, bmp)

def get_isle():
    return read_svg('data/bornholm.svg')[0]

isle = get_isle()
gb = get_GB
n = get_norwae()