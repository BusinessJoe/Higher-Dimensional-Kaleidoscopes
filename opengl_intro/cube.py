import time

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtOpenGL

import OpenGL.GL as gl
import numpy as np

import sys
import ctypes

from load_shader import Shader
import transformations as trans


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.resize(300, 300)
        self.setWindowTitle("Hello OpenGL App")

        self.glWidget = GLWidget(self)
        self.initGUI()

        timer = QtCore.QTimer(self)
        timer.setInterval(20)
        timer.timeout.connect(self.glWidget.updateGL)
        timer.start()

    def initGUI(self):
        central_widget = QtWidgets.QWidget()
        gui_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(gui_layout)
        self.setCentralWidget(central_widget)
        gui_layout.addWidget(self.glWidget)


class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.parent = parent

        self.angle = 0
        self.light_pos = np.array([0.0, 1.0, 2], np.float32)

    def initializeGL(self) -> None:
        gl.glEnable(gl.GL_DEPTH_TEST)

        self.lightingShader = Shader("light_shader.vs", "light_shader.fs")
        self.lightCubeShader = Shader("light_cube.vs", "light_cube.fs")

        # positions followed by rgb values
        vertices = np.array([
            -0.5, -0.5, -0.5, 0.0, 0.0, -1.0,
            0.5, -0.5, -0.5, 0.0, 0.0, -1.0,
            0.5, 0.5, -0.5, 0.0, 0.0, -1.0,
            0.5, 0.5, -0.5, 0.0, 0.0, -1.0,
            -0.5, 0.5, -0.5, 0.0, 0.0, -1.0,
            -0.5, -0.5, -0.5, 0.0, 0.0, -1.0,

            -0.5, -0.5, 0.5, 0.0, 0.0, 1.0,
            0.5, -0.5, 0.5, 0.0, 0.0, 1.0,
            0.5, 0.5, 0.5, 0.0, 0.0, 1.0,
            0.5, 0.5, 0.5, 0.0, 0.0, 1.0,
            -0.5, 0.5, 0.5, 0.0, 0.0, 1.0,
            -0.5, -0.5, 0.5, 0.0, 0.0, 1.0,

            -0.5, 0.5, 0.5, -1.0, 0.0, 0.0,
            -0.5, 0.5, -0.5, -1.0, 0.0, 0.0,
            -0.5, -0.5, -0.5, -1.0, 0.0, 0.0,
            -0.5, -0.5, -0.5, -1.0, 0.0, 0.0,
            -0.5, -0.5, 0.5, -1.0, 0.0, 0.0,
            -0.5, 0.5, 0.5, -1.0, 0.0, 0.0,

            0.5, 0.5, 0.5, 1.0, 0.0, 0.0,
            0.5, 0.5, -0.5, 1.0, 0.0, 0.0,
            0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
            0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
            0.5, -0.5, 0.5, 1.0, 0.0, 0.0,
            0.5, 0.5, 0.5, 1.0, 0.0, 0.0,

            -0.5, -0.5, -0.5, 0.0, -1.0, 0.0,
            0.5, -0.5, -0.5, 0.0, -1.0, 0.0,
            0.5, -0.5, 0.5, 0.0, -1.0, 0.0,
            0.5, -0.5, 0.5, 0.0, -1.0, 0.0,
            -0.5, -0.5, 0.5, 0.0, -1.0, 0.0,
            -0.5, -0.5, -0.5, 0.0, -1.0, 0.0,

            -0.5, 0.5, -0.5, 0.0, 1.0, 0.0,
            0.5, 0.5, -0.5, 0.0, 1.0, 0.0,
            0.5, 0.5, 0.5, 0.0, 1.0, 0.0,
            0.5, 0.5, 0.5, 0.0, 1.0, 0.0,
            -0.5, 0.5, 0.5, 0.0, 1.0, 0.0,
            -0.5, 0.5, -0.5, 0.0, 1.0, 0.0
        ], np.float32)
        # cube offsets
        self.cube_offsets = np.array([
            [0.0, 0.0, 0.0],
            [2.0, 5.0, -15.0],
            [-1.5, -2.2, -2.5],
            [-3.8, -.0, -12.3],
        ], np.float32)

        # first, configure the cube's VAO and VBO
        self.cube_vertex_array = gl.glGenVertexArrays(1)
        self.vertex_buffer = gl.glGenBuffers(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vertex_buffer)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, len(vertices) * 4, vertices, gl.GL_STATIC_DRAW)

        gl.glBindVertexArray(self.cube_vertex_array)

        # position attribute
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 6 * 4, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)
        # normal attribute
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FLOAT, 6 * 4, ctypes.c_void_p(3 * 4))
        gl.glEnableVertexAttribArray(1)

        # second, configure the light's VAO (VBO stays the same)
        self.light_cube_VAO = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.light_cube_VAO)

        # we only need to bind to the VBO (to link it with glVertexAttribPointer)
        # no need to fill it; the VBO's data already contains all we need
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vertex_buffer)

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 6 * 4, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)

    def paintGL(self):
        gl.glClearColor(0.1, 0.1, 0.1, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # change light's position
        self.light_pos[0] = np.sin(3*self.angle) * 2
        self.light_pos[2] = np.cos(3*self.angle) * 2

        self.lightingShader.use()
        self.lightingShader.set_vec3("objectColor", 1.0, 0.5, 0.31)
        self.lightingShader.set_vec3("lightColor", 1.0, 1.0, 1.0)
        self.lightingShader.set_vec3v("lightPos", self.light_pos)

        # view/projection transforms
        projection = trans.perspective(np.radians(45), self.width() / self.height(), 0.1, 100.0)
        view = trans.translate(np.identity(4), np.array((0, 0, -3), np.float32))
        view = trans.rotate(view, np.radians(45), np.array((0, 1, 0), np.float32))
        self.lightingShader.set_mat4("projection", projection)
        self.lightingShader.set_mat4("view", view)

        # world transformation
        model = np.identity(4)
        self.lightingShader.set_mat4("model", model)

        # render the cube
        gl.glBindVertexArray(self.cube_vertex_array)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 36)

        # also draw the lamp object
        self.lightCubeShader.use()
        self.lightCubeShader.set_mat4("projection", projection)
        self.lightCubeShader.set_mat4("view", view)
        model = np.identity(4)
        model = trans.translate(model, self.light_pos)
        model = trans.scale(model, np.array([0.5, 0.5, 0.5], np.float32))
        self.lightCubeShader.set_mat4("model", model)

        gl.glBindVertexArray(self.light_cube_VAO)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 36)
        # gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))
        # gl.glBindVertexArray(0)

    def resizeGL(self, w: int, h: int) -> None:
        gl.glViewport(0, 0, w, h)
        # gl.glMatrixMode(gl.GL_PROJECTION)
        # gl.glLoadIdentity()

        # aspect = w / h
        # GLU.gluPerspective(45, aspect, 1, 100)
        # gl.glMatrixMode(gl.GL_MODELVIEW)

    def updateGL(self) -> None:
        time_value = time.time()
        self.angle = time_value * np.radians(50)
        self.repaint()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())
