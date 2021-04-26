import numpy as np
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

from polytope_visualizer.math.project_down import v_project
from polytope_visualizer.math.rotate import v_rotate

import math


class RenderArea(QFrame):
    """Handles rendering of 3d points"""

    def __init__(self, width, height):
        super().__init__()

        self.projected_points = []

        self.points = []

        self.width, self.height = width, height
        self.setMinimumSize(width, height)

        self.setStyleSheet("""border:2px solid rgb(0, 0, 0);
        """)

        self.scaling = 100
        self.dot_size = 20
        self.screen_dist = 300
        self.eye_dist = 600

        # Set up a zero array for the angles
        self.angles_3d = [0.0, 0.0, 0.0]

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setBrush(Qt.white)
        self._draw_points(qp)
        qp.end()

    def _draw_points(self, qp):
        for p in self.projected_points:
            qp.drawEllipse(int(p[0] - p[2] + self.width / 2),
                           int(p[1] - p[2] + self.height / 2),
                           int(2 * p[2]),
                           int(2 * p[2]))

    def set_points(self, points):
        self.points = points
        self.draw_polytope()
        self.update()

    def draw_polytope(self):
        self.projected_points = self._project_points(self.points)

    def _project_points(self, points):
        proj_points = v_rotate(points, float(math.radians(self.angles_3d[0])), 0, 1)
        proj_points = v_rotate(proj_points, float(math.radians(self.angles_3d[1])), 0, 2)
        proj_points = v_rotate(proj_points, float(math.radians(self.angles_3d[2])), 1, 2)

        proj_points, heights = v_project(proj_points, self.screen_dist, self.eye_dist)

        heights = np.reshape(heights, (-1, 1))
        heights *= self.dot_size

        points_and_heights = np.concatenate((proj_points, heights), axis=1)

        # Sort points based on distance to camera
        indices = np.argsort(heights, axis=0)
        sorted_points_and_heights = np.take_along_axis(points_and_heights, indices, axis=0)

        return sorted_points_and_heights
