import math
from functools import partial

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QFrame, QSlider, QGridLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

import numpy as np
from src.polytope_visualizer.project_down import v_project
from src.polytope_visualizer.rotate import v_rotate
from src.polytope_visualizer.diagram import CoxeterDiagram


class Renderer(QWidget):
    def __init__(self, diagram: CoxeterDiagram):
        super().__init__()
        # self.iterations = 10
        #
        self.diagram = diagram
        self.points = diagram.polytope()
        self.width = 600
        self.height = 600

        self.scaling = 100
        self.dot_size = 20
        self.screen_dist = 300
        self.eye_dist = 600

        # Set up a zero array for the angles
        self.angles = [0, 0, 0]

        self.canvas = RenderArea(self.width, self.height)
        self.init_ui()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.draw_polytope)
        self.timer.start(1000//60)

    def init_ui(self):
        vlayout = QVBoxLayout()
        grid = QGridLayout()

        vlayout.addWidget(self.canvas)

        for i in range(3):
            angle_slider = QSlider(Qt.Horizontal)
            angle_slider.setMinimum(0)
            angle_slider.setMaximum(360)
            angle_slider.setMaximumWidth(200)
            angle_slider.valueChanged.connect(partial(self.update_angle, i))
            grid.addWidget(angle_slider, i, 0)

        # Scale slider
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(300)
        slider.setValue(self.scaling)
        slider.setMaximumWidth(200)
        slider.valueChanged.connect(self.set_scale)
        grid.addWidget(slider, 0, 1)

        # Screen dist slider
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(1000)
        slider.setValue(self.screen_dist)
        slider.setMaximumWidth(200)
        slider.valueChanged.connect(self.set_screen_dist)
        grid.addWidget(slider, 1, 1)

        # Eye dist slider
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(1000)
        slider.setValue(self.eye_dist)
        slider.setMaximumWidth(200)
        slider.valueChanged.connect(self.set_eye_dist)
        grid.addWidget(slider, 2, 1)

        # Dot size slider
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(self.dot_size)
        slider.setMaximumWidth(200)
        slider.valueChanged.connect(self.set_dot_size)
        grid.addWidget(slider, 0, 2)

        vlayout.addLayout(grid)
        self.setLayout(vlayout)

    def draw_polytope(self):
        rotated_points = self.points * self.scaling

        rotated_points = v_rotate(rotated_points, float(self.angles[0]), 0, 1, self.diagram.dimension)
        rotated_points = v_rotate(rotated_points, float(self.angles[1]), 0, 2, self.diagram.dimension)
        rotated_points = v_rotate(rotated_points, float(self.angles[2]), 1, 2, self.diagram.dimension)

        proj_points = np.copy(rotated_points)
        while proj_points.shape[1] != 2:
            proj_points, heights = v_project(proj_points, self.screen_dist, self.eye_dist)

        heights = np.reshape(heights, (-1, 1))
        heights *= self.dot_size

        points_and_heights = np.concatenate((proj_points, heights), axis=1)

        # Sort points based on distance to camera
        indices = np.argsort(heights, axis=0)
        sorted_points_and_heights = np.take_along_axis(points_and_heights, indices, axis=0)

        self.canvas.set_points(sorted_points_and_heights)

    def set_diagram(self, diagram: CoxeterDiagram):
        self.diagram = diagram
        self.points = diagram.polytope()

    def update_angle(self, index, value):
        self.angles[index] = value * math.pi / 180

    def set_scale(self, scale):
        self.scaling = scale

    def set_dot_size(self, size):
        self.dot_size = size

    def set_screen_dist(self, dist):
        self.screen_dist = dist

    def set_eye_dist(self, dist):
        self.eye_dist = dist


class RenderArea(QFrame):
    def __init__(self, width, height):
        super().__init__()

        self.points = []

        self.width, self.height = width, height
        self.setMinimumSize(width, height)

        self.setStyleSheet("""border:2px solid rgb(0, 0, 0);
        """)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setBrush(Qt.white)
        self.draw_points(qp)
        qp.end()

    def draw_points(self, qp):
        for p in self.points:
            qp.drawEllipse(int(p[0] - p[2] + self.width / 2),
                           int(p[1] - p[2] + self.height / 2),
                           int(2 * p[2]),
                           int(2 * p[2]))

    def set_points(self, points):
        self.points = points
        self.update()
