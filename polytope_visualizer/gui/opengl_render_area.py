from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtOpenGL

import OpenGL.GL as gl
from OpenGL import GLU

from OpenGL.arrays import vbo       # vertex buffer objects
import numpy as np

import sys


class OpenGLRenderArea(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.parent = parent
        self.points = None

        self.scaling = 100
        self.dot_size = 20
        self.screen_dist = 300
        self.eye_dist = 600

        # Set up a zero array for the angles
        self.angles_3d = [0.0, 0.0, 0.0]

    def set_points(self, points):
        self.points = points
        self.updateGL()

    def initializeGL(self) -> None:
        gl.glEnable(gl.GL_DEPTH_TEST)                   # enable depth testing
        self.init_geometry()

    def resizeGL(self, w: int, h: int) -> None:
        gl.glViewport(0, 0, w, h)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()

        aspect = w / h
        GLU.gluPerspective(45, aspect, 1, 100)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def paintGL(self) -> None:
        print(self.angles_3d)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        for point in self.points:
            x, y, z = point[0], point[1], point[2]
            self.cube(x, y, z, radius=self.dot_size)

    def cube(self, x, y, z, radius):
        gl.glPushMatrix()  # push the current matrix to the current stack

        # transformations are applied in reverse order
        gl.glTranslate(0.0, 0.0, -50.0)  # translate cube to specified depth
        gl.glRotate(self.angles_3d[0], 1, 0, 0)
        gl.glRotate(self.angles_3d[1], 0, 1, 0)
        gl.glRotate(self.angles_3d[2], 0, 0, 1)
        gl.glTranslate(x/10, y/10, z/10)  # offset cube
        gl.glScale(radius, radius, radius)  # scale cube
        gl.glTranslate(-0.5, -0.5, -0.5)  # translate cube center to origin

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)

        gl.glVertexPointer(3, gl.GL_FLOAT, 0, self.vert_VBO)
        gl.glColorPointer(3, gl.GL_FLOAT, 0, self.color_VBO)

        gl.glDrawElements(gl.GL_QUADS, len(self.cube_idx_array), gl.GL_UNSIGNED_INT, self.cube_idx_array)

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)

        gl.glPopMatrix()  # restore the previous modelview matrix

    def init_geometry(self):
        self.cube_vtx_array = np.array(
            [[0.0, 0.0, 0.0],
             [1.0, 0.0, 0.0],
             [1.0, 1.0, 0.0],
             [0.0, 1.0, 0.0],
             [0.0, 0.0, 1.0],
             [1.0, 0.0, 1.0],
             [1.0, 1.0, 1.0],
             [0.0, 1.0, 1.0]]
        )
        self.vert_VBO = vbo.VBO(np.reshape(self.cube_vtx_array,
                                           (1, -1)).astype(np.float32))
        self.vert_VBO.bind()

        self.cube_clr_array = np.array(
            [[0.0, 0.0, 0.0],
             [1.0, 0.0, 0.0],
             [1.0, 1.0, 0.0],
             [0.0, 1.0, 0.0],
             [0.0, 0.0, 1.0],
             [1.0, 0.0, 1.0],
             [1.0, 1.0, 1.0],
             [0.0, 1.0, 1.0]]
        )
        self.color_VBO = vbo.VBO(np.reshape(self.cube_clr_array, (1, -1)).astype(np.float32))
        self.color_VBO.bind()

        self.cube_idx_array = np.array(
            [0, 1, 2, 3,
             3, 2, 6, 7,
             1, 0, 4, 5,
             2, 1, 5, 6,
             0, 3, 7, 4,
             7, 6, 5, 4]
        )
