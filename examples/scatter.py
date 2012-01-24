import numpy as np
from wxpy3d import PointWindow, wxApp

window = PointWindow(title='Scatter Test', size=(500,500))

def scatter():
    xyz = -1+2*np.random.rand(100,3).astype('f')
    rgba = np.random.rand(100,4).astype('f')
    window.update_points(xyz, rgba)
    window.Refresh()
    
scatter()

# If you're using IPython, comment out the following line. Then you can
# run the script with
#      ipython -pylab -wthread -i examples/scatter.py
# Notice that the window still processes events in the background while
# you use the command line. You can call
#      scatter()
# as many times as you like.
#

# wxApp.MainLoop()
