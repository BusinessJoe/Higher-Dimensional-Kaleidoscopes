from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtOpenGL

import OpenGL.GL as gl
from OpenGL import GLU
from OpenGL.GL import shaders

from OpenGL.arrays import vbo       # vertex buffer objects
import numpy as np

import sys


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

        sliderX = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sliderX.valueChanged.connect(lambda val: self.glWidget.setRotX(val))
        sliderX.setMinimum(0)
        sliderX.setMaximum(360)

        sliderY = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sliderY.valueChanged.connect(lambda val: self.glWidget.setRotY(val))
        sliderY.setMinimum(0)
        sliderY.setMaximum(360)

        sliderZ = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sliderZ.valueChanged.connect(lambda val: self.glWidget.setRotZ(val))
        sliderZ.setMinimum(0)
        sliderZ.setMaximum(360)

        gui_layout.addWidget(sliderX)
        gui_layout.addWidget(sliderY)
        gui_layout.addWidget(sliderZ)


class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.parent = parent

    def initializeGL(self) -> None:
        self.qglClearColor(QtGui.QColor(0, 0, 255))     # initialize screen to blue
        gl.glEnable(gl.GL_DEPTH_TEST)                   # enable depth testing

        # Shaders
        with open('polytope_visualizer/shader') as f:
            vertexShaderSource = f.read()

        # vertexShader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        # gl.glShaderSource(vertexShader, 1, vertexShaderSource, 0)
        # gl.glCompileShader(vertexShader)
        vertexShader = shaders.compileShader(vertexShaderSource, gl.GL_VERTEX_SHADER)
        success = gl.glGetShaderiv(vertexShader, gl.GL_COMPILE_STATUS)
        if not success:
            infoLog = gl.glGetShaderInfoLog(vertexShader, 512, None)
            print(infoLog)

        fragmentShaderSource = """#version 330 core
out vec4 FragColor;

void main()
{
    FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
} """

        # fragmentShader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        # gl.glShaderSource(fragmentShader, 1, fragmentShaderSource, None)
        # gl.glCompileShader(fragmentShader)
        fragmentShader = shaders.compileShader(fragmentShaderSource, gl.GL_FRAGMENT_SHADER)

        # self.shaderProgram = gl.glCreateProgram()
        # gl.glAttachShader(self.shaderProgram, vertexShader)
        # gl.glAttachShader(self.shaderProgram, fragmentShader)
        # gl.glLinkProgram(self.shaderProgram)
        self.shaderProgram = shaders.compileProgram(vertexShader, fragmentShader)

        gl.glDeleteShader(vertexShader)
        gl.glDeleteShader(fragmentShader)

        self.init_geometry()

        self.rotX = 0.0
        self.rotY = 0.0
        self.rotZ = 0.0

    def resizeGL(self, w: int, h: int) -> None:
        gl.glViewport(0, 0, w, h)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()

        aspect = w / h
        GLU.gluPerspective(45, aspect, 1, 100)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def paintGL(self):
        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        gl.glUseProgram(self.shaderProgram)
        gl.glBindVertexArray(self.VAO)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)

        # self.cube(-10)
        # self.cube(10)

    def init_geometry(self):

        vertices = np.array([
            -0.5, -0.5, 0.0,
             0.5, -0.5, 0.0,
             0.0,  0.5, 0.0
        ], np.float32)

        self.VAO = gl.glGenVertexArrays(1)
        self.VBO = gl.glGenBuffers(1)

        gl.glBindVertexArray(self.VAO)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.VBO)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, len(vertices), vertices, gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 3, 0)
        gl.glEnableVertexAttribArray(0)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

        gl.glBindVertexArray(0)

    def setRotX(self, val):
        self.rotX = val

    def setRotY(self, val):
        self.rotY = val

    def setRotZ(self, val):
        self.rotZ = val


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())
