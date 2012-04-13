from OpenGL.GL import *

from contextlib import contextmanager
@contextmanager
def opengl_attrib():
    try:
        glPushClientAttrib(GL_CLIENT_ALL_ATTRIB_BITS)
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        yield
    finally:
        glPopClientAttrib(GL_CLIENT_ALL_ATTRIB_BITS)
        glPopAttrib(GL_ALL_ATTRIB_BITS)

@contextmanager
def opengl_matrix():
    try:
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        yield
    finally:
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

@contextmanager
def opengl_state():
    with opengl_attrib():
        with opengl_matrix():
            yield
