import math
from functools import partial

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout
from PyQt5.QtCore import Qt

import numpy as np
from polytope_visualizer.math.project_down import v_project, project_3d
from polytope_visualizer.math.rotate import v_rotate
from polytope_visualizer.math.diagram import CoxeterDiagram
from .slider import LabelledSlider
from .render_area import RenderArea


class Renderer(QWidget):
    def __init__(self, diagram: CoxeterDiagram):
        super().__init__()
        # self.iterations = 10
        #
        self.diagram = diagram
        self.points = diagram.polytope()
        self.width = 600
        self.height = 600

        self.rotors = []

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
            angle_slider = LabelledSlider("Angle", Qt.Horizontal)
            angle_slider.sl.setMinimum(0)
            angle_slider.sl.setMaximum(360)
            angle_slider.sl.setMaximumWidth(200)
            angle_slider.sl.valueChanged.connect(partial(self.update_angle, i))
            grid.addWidget(angle_slider, i, 0)

        # Scale slider
        slider = LabelledSlider("Scale", Qt.Horizontal)
        slider.sl.setMinimum(0)
        slider.sl.setMaximum(300)
        slider.sl.setValue(self.canvas.scaling)
        slider.sl.setMaximumWidth(200)
        slider.sl.valueChanged.connect(self.set_scale)
        grid.addWidget(slider, 0, 1)

        # Screen dist slider
        slider = LabelledSlider("Screen Distance", Qt.Horizontal)
        slider.sl.setMinimum(0)
        slider.sl.setMaximum(1000)
        slider.sl.setValue(self.canvas.screen_dist)
        slider.sl.setMaximumWidth(200)
        slider.sl.valueChanged.connect(self.set_screen_dist)
        grid.addWidget(slider, 1, 1)

        # Eye dist slider
        slider = LabelledSlider("Eye Distance", Qt.Horizontal)
        slider.sl.setMinimum(0)
        slider.sl.setMaximum(1000)
        slider.sl.setValue(self.canvas.eye_dist)
        slider.sl.setMaximumWidth(200)
        slider.sl.valueChanged.connect(self.set_eye_dist)
        grid.addWidget(slider, 2, 1)

        # Dot size slider
        slider = LabelledSlider("Dot Size", Qt.Horizontal)
        slider.sl.setMinimum(0)
        slider.sl.setMaximum(100)
        slider.sl.setValue(self.canvas.dot_size)
        slider.sl.setMaximumWidth(200)
        slider.sl.valueChanged.connect(self.set_dot_size)
        grid.addWidget(slider, 0, 2)

        vlayout.addLayout(grid)
        self.setLayout(vlayout)

    def draw_polytope(self):
        rotated_points = self.points * self.canvas.scaling

        # Do pre-projection rotations here
        for r in self.rotors:
            try:
                rotated_points = r.rotate(rotated_points)
            except IndexError:
                pass

        # Post-projection rotations happen in 3d
        proj_points = np.copy(rotated_points)
        proj_points = project_3d(proj_points)

        self.canvas.set_points(proj_points)

    def set_diagram(self, diagram: CoxeterDiagram):
        self.diagram = diagram
        self.points = diagram.polytope()

    def update_angle(self, index, value):
        self.canvas.angles_3d[index] = value * math.pi / 180

    def set_scale(self, scale):
        self.canvas.scaling = scale

    def set_dot_size(self, size):
        self.canvas.dot_size = size

    def set_screen_dist(self, dist):
        self.canvas.screen_dist = dist

    def set_eye_dist(self, dist):
        self.canvas.eye_dist = dist

    def set_rotors(self, rotors):
        self.rotors = rotors
