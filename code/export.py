import matplotlib.pyplot as plt
from fracgen import sierpinsky
import numpy as np

pts = sierpinsky(7)
name ='vonkoch1'
# name =sierpinski1
fig, ax = plt.subplots(figsize=(30, 30),frameon=False)
ax.set_axis_off()
ax.set_aspect(1)
ax.plot(pts[:,0],pts[:,1],linewidth=.1,)
fig.savefig(name+'.svg',format="svg", dpi=300, bbox_inches="tight", pad_inches=0) #png/svg/pdf
# fig.canvas.draw()
# w,h = fig.canvas.get_width_height()
# buf = np.frombuffer ( fig.canvas.buffer_rgba(), dtype=np.uint8 )
# buf = buf.reshape((w,h,-1))
# print(buf.shape)
# plt.imshow(buf[:,:,:3])

