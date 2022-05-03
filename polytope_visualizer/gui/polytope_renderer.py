import math
from functools import partial

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QCheckBox
from PyQt5.QtCore import Qt

import numpy as np
from polytope_visualizer.math.project_down import project_3d
from polytope_visualizer.math.diagram import CoxeterDiagram
from .slider import LabelledSlider
from .opengl_render_area import OpenGLRenderArea


class Renderer(QWidget):
    def __init__(self, diagram: CoxeterDiagram):
        super().__init__()
        # self.iterations = 10
        #
        self.diagram = diagram
        self.points, edges = diagram.polytope()
        self.width = 600
        self.height = 600

        self.rotors = []

        self.canvas = OpenGLRenderArea()
        self.canvas.setFixedWidth(self.width)
        self.canvas.setFixedHeight(self.height)
        self.canvas.show()
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
            angle_slider.sl.valueChanged.connect(partial(self.canvas.set_angle, i))
            grid.addWidget(angle_slider, i, 0)

        # Scale slider
        slider = LabelledSlider("Scale", Qt.Horizontal)
        slider.sl.setMinimum(0)
        slider.sl.setMaximum(15)
        slider.sl.setValue(self.canvas.scaling)
        slider.sl.setMaximumWidth(200)
        slider.sl.valueChanged.connect(self.canvas.set_scale)
        grid.addWidget(slider, 0, 1)

        # Distance slider
        slider = LabelledSlider("Distance", Qt.Horizontal)
        slider.sl.setMinimum(0)
        slider.sl.setMaximum(150)
        slider.sl.setValue(self.canvas.distance)
        slider.sl.setMaximumWidth(200)
        slider.sl.valueChanged.connect(self.canvas.set_distance)
        grid.addWidget(slider, 1, 1)

        # Radius slider
        slider = LabelledSlider("Radius", Qt.Horizontal)
        slider.sl.setMinimum(0)
        slider.sl.setMaximum(100)
        slider.sl.setValue(self.canvas.radius*10)
        slider.sl.setMaximumWidth(200)
        slider.sl.valueChanged.connect(lambda val: self.canvas.set_radius(val/10))
        grid.addWidget(slider, 2, 1)

        # Lighting checkbox
        checkbox = QCheckBox("Lighting")
        checkbox.stateChanged.connect(lambda state: self.canvas.set_shading(state))
        grid.addWidget(checkbox, 3, 1)

        vlayout.addLayout(grid)
        self.setLayout(vlayout)

    def draw_polytope(self):
        rotated_points = self.points

        # Do pre-projection rotations here
        for r in self.rotors:
            try:
                rotated_points = r.rotate(rotated_points)
            except IndexError:
                pass

        # Post-projection rotations happen in 3d
        proj_points = np.copy(rotated_points)
        proj_points = project_3d(proj_points)

        norm = np.linalg.norm(proj_points[0])

        self.canvas.set_points(self.canvas.scaling * proj_points / norm)

    def set_diagram(self, diagram: CoxeterDiagram):
        self.diagram = diagram
        self.points, edges = diagram.polytope()

    def set_rotors(self, rotors):
        self.rotors = rotors
