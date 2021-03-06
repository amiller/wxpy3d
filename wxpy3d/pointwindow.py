from camerawindow import CameraWindow
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.ARB.vertex_buffer_object import *

TEXTURE_TARGET = GL_TEXTURE_RECTANGLE


# Window for drawing point clouds
class PointWindow(CameraWindow):

    def __init__(self, *args, **kwargs):
        self.XYZ = np.zeros((0,3))
        self.RGBA = None
        self.N = None
        self.clearcolor = [1,1,1,0]
        super(PointWindow,self).__init__(*args, **kwargs)

    def on_init(self):
        self.create_buffers()

    def create_buffers(self):
        if 'rgbtex' in self.__dict__:
            raise Exception('Buffers already created [pointwindow]')
        self.rgbtex = glGenTextures(1)
        glBindTexture(TEXTURE_TARGET, self.rgbtex)
        glTexImage2D(TEXTURE_TARGET,0,GL_RGB,640,480,0,GL_RGB,
                     GL_UNSIGNED_BYTE,None)

        self._depth = np.empty((480,640,3),np.int16)
        self._depth[:,:,1], self._depth[:,:,0] = np.mgrid[:480,:640]
        self.xyzbuf = glGenBuffersARB(1)
        glBindBufferARB(GL_ARRAY_BUFFER_ARB, self.xyzbuf)
        glBufferDataARB(GL_ARRAY_BUFFER_ARB, 640*480*3*4, None,GL_DYNAMIC_DRAW)
        self.rgbabuf = glGenBuffersARB(1)
        glBindBufferARB(GL_ARRAY_BUFFER_ARB, self.rgbabuf)
        glBufferDataARB(GL_ARRAY_BUFFER_ARB, 640*480*4*4, None,GL_DYNAMIC_DRAW)
        self.normalsbuf = glGenBuffersARB(1)
        glBindBufferARB(GL_ARRAY_BUFFER_ARB, self.normalsbuf)
        glBufferDataARB(GL_ARRAY_BUFFER_ARB, 640*480*4*3, None,GL_DYNAMIC_DRAW)


    def update_points(self, XYZ=None, RGBA=None, N=None):
        if XYZ is None: XYZ = np.zeros((0,3),'f')
        # TODO make this more elegant, coerce RGBA to match XYZ somehow
        assert XYZ.dtype == np.float32
        assert RGBA is None or RGBA.dtype == np.float32
        assert XYZ.shape[1] == 3
        assert RGBA is None or RGBA.shape[1] == 4
        assert RGBA is None or XYZ.shape[0] == RGBA.shape[0]
        self.XYZ = XYZ
        self.RGBA = RGBA
        self.N = N
        self.canvas.SetCurrent()
        glBindBufferARB(GL_ARRAY_BUFFER_ARB, self.xyzbuf)
        glBufferSubDataARB(GL_ARRAY_BUFFER_ARB, 0, XYZ.shape[0]*3*4, XYZ)
        if not RGBA is None:
            glBindBufferARB(GL_ARRAY_BUFFER_ARB, self.rgbabuf)
            glBufferSubDataARB(GL_ARRAY_BUFFER_ARB, 0, XYZ.shape[0]*4*4, RGBA)
        elif not N is None:
            glBindBufferARB(GL_ARRAY_BUFFER_ARB, self.normalsbuf)
            glBufferSubDataARB(GL_ARRAY_BUFFER_ARB, 0, XYZ.shape[0]*4*3, N)            
        glBindBufferARB(GL_ARRAY_BUFFER_ARB, 0)

    def update_xyz(self,X,Y,Z,COLOR=None,AXES=None):
        xyz = np.vstack((X.flatten(),Y.flatten(),Z.flatten())).transpose()
        mask = Z.flatten()<10
        xyz = xyz[mask,:]

        global axes_rotation
        axes_rotation = np.eye(4)
        if not AXES is None:
            # Rotate the axes
            axes_rotation[:3,:3] = expmap.axis2rot(-AXES)
            window.upvec = axes_rotation[:3,1]

        if not COLOR is None:
            R,G,B,A = COLOR
            color = np.vstack((R.flatten(),
                               G.flatten(),
                               B.flatten(),
                               A.flatten())).transpose()
            color = color[mask,:]
        else:
            assert not COLOR is None, "FIXME: empty color not implemented"

        self.update_points(xyz, color)

    def draw_points(self):
        glBindBufferARB(GL_ARRAY_BUFFER_ARB, self.xyzbuf)
        glVertexPointerf(None)
        glEnableClientState(GL_VERTEX_ARRAY)
        if not self.RGBA is None:
            glBindBufferARB(GL_ARRAY_BUFFER_ARB, self.rgbabuf)
            glColorPointer(4, GL_FLOAT, 0, None)
            glEnableClientState(GL_COLOR_ARRAY)            
        if not self.N is None:
            glBindBufferARB(GL_ARRAY_BUFFER_ARB, self.normalsbuf)
            glNormalPointer(GL_FLOAT, 0, None)
            glEnableClientState(GL_NORMAL_ARRAY)
        if not self.XYZ is None:
            # Draw the points
            glPointSize(2)
            glDrawElementsui(GL_POINTS, np.arange(len(self.XYZ)))
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)            
        glDisableClientState(GL_VERTEX_ARRAY)
        glBindBufferARB(GL_ARRAY_BUFFER_ARB, 0)
        glDisable(GL_BLEND)

    def on_draw(self):
        super(PointWindow,self).set_camera()

        glClearColor(*self.clearcolor)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        self._wrap('pre_draw')

        self.draw_points()

        self._wrap('post_draw')
