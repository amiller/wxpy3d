Wraps wxPython to get you an OpenGL context without much fuss. Useful for 3D visualizations.

Example
-------
    import numpy as np
    from wxpy3d import PointWindow

    window = PointWindow(title='Scatter Test', size=(500,500))

    # Make some points (and colors)
    xyz = -1+2*np.random.rand(100,3).astype('f')
    rgba = np.random.rand(100,4).astype('f')

    window.update_points(xyz, rgba)
    window.Refresh()

    
Files
-----
- wxpy3d.Window: 
   - A window with an OpenGL context in it
- wxpy3d.CameraWindow (extends Window): 
   - A window that responds mouse events by manipulating a *camera matrix*
- wxpy3d.PointWindow (extends CameraWindow): 
   - Uses a vertex array buffer to efficiently draw a point cloud (numpy array)


Requirements
------------
wxWidgets (with OpenGL)

wxPython

PyOpenGL

numpy