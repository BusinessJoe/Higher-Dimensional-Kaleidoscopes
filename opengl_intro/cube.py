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

    def initializeGL(self) -> None:
        gl.glEnable(gl.GL_DEPTH_TEST)

        shader = Shader("shader.vert", "shader.frag")
        self.program = shader.use()

        # positions followed by rgb values
        vertices = np.array([
            -0.5, -0.5, -0.5, 0.0, 0.0,
            0.5, -0.5, -0.5, 0.0, 0.2,
            0.5, 0.5, -0.5, 0.0, 0.4,
            0.5, 0.5, -0.5, 0.0, 0.6,
            -0.5, 0.5, -0.5, 0.0, 0.8,
            -0.5, -0.5, -0.5, 0.0, 1.0,

            -0.5, -0.5, 0.5, 0.2, 0.0,
            0.5, -0.5, 0.5, 0.2, 0.2,
            0.5, 0.5, 0.5, 0.2, 0.4,
            0.5, 0.5, 0.5, 0.2, 0.6,
            -0.5, 0.5, 0.5, 0.2, 0.8,
            -0.5, -0.5, 0.5, 0.2, 1.0,

            -0.5, 0.5, 0.5, 0.4, 0.0,
            -0.5, 0.5, -0.5, 0.4, 0.2,
            -0.5, -0.5, -0.5, 0.4, 0.4,
            -0.5, -0.5, -0.5, 0.4, 0.6,
            -0.5, -0.5, 0.5, 0.4, 0.8,
            -0.5, 0.5, 0.5, 0.4, 1.0,

            0.5, 0.5, 0.5, 0.6, 0.0,
            0.5, 0.5, -0.5, 0.6, 0.2,
            0.5, -0.5, -0.5, 0.6, 0.4,
            0.5, -0.5, -0.5, 0.6, 0.6,
            0.5, -0.5, 0.5, 0.6, 0.8,
            0.5, 0.5, 0.5, 0.6, 1.0,

            -0.5, -0.5, -0.5, 0.8, 0.0,
            0.5, -0.5, -0.5, 0.8, 0.2,
            0.5, -0.5, 0.5, 0.8, 0.4,
            0.5, -0.5, 0.5, 0.8, 0.6,
            -0.5, -0.5, 0.5, 0.8, 0.8,
            -0.5, -0.5, -0.5, 0.8, 1.0,

            -0.5, 0.5, -0.5, 1.0, 0.0,
            0.5, 0.5, -0.5, 1.0, 0.2,
            0.5, 0.5, 0.5, 1.0, 0.4,
            0.5, 0.5, 0.5, 1.0, 0.6,
            -0.5, 0.5, 0.5, 1.0, 0.8,
            -0.5, 0.5, -0.5, 1.0, 1.0,
        ], np.float32)
        # indices = np.array([
        #     0, 1, 3,
        #     1, 2, 3,
        # ], np.uint32)

        self.vertex_array = gl.glGenVertexArrays(1)
        self.vertex_buffer = gl.glGenBuffers(1)
        # self.element_buffer = gl.glGenBuffers(1)

        # 1. bind Vertex Array Object
        gl.glBindVertexArray(self.vertex_array)
        # 2. copy our vertices array in a buffer for OpenGL to use
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vertex_buffer)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, len(vertices) * 4, vertices, gl.GL_STATIC_DRAW)
        # 3. copy our index array in a element buffer for OpenGL to use
        # gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.element_buffer)
        # gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, len(indices) * 4, indices, gl.GL_STATIC_DRAW)
        # 4. then set our vertex attributes pointers
        # position attribute
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 5 * 4, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)
        # color attribute
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 2 * 4, ctypes.c_void_p(5 * 4))
        gl.glEnableVertexAttribArray(1)

        # gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        # gl.glBindVertexArray(0)

        # gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)

    def paintGL(self):
        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glUseProgram(self.program)

        # create transformations
        model = np.identity(4)
        view = np.identity(4)
        projection = np.identity(4)
        model = trans.rotate(model, self.angle, np.array((0.5, 1.0, 0), np.float32))
        view = trans.translate(view, np.array((0, 0, -3), np.float32))
        projection = trans.perspective(np.radians(45), self.width() / self.height(), 0.1, 100.0)
        # retrieve the matrix uniform locations
        model_loc = gl.glGetUniformLocation(self.program, "model")
        view_loc = gl.glGetUniformLocation(self.program, "view")
        projection_loc = gl.glGetUniformLocation(self.program, "projection")
        # pass them to the shaders
        gl.glUniformMatrix4fv(model_loc, 1, gl.GL_FALSE, model)
        gl.glUniformMatrix4fv(view_loc, 1, gl.GL_FALSE, view)
        gl.glUniformMatrix4fv(projection_loc, 1, gl.GL_FALSE, projection)

        # render
        gl.glBindVertexArray(self.vertex_array)
        # gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 36)
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
