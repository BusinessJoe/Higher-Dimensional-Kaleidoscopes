import tkinter as tk
import math
import numpy as np
from src.polytope_visualizer.project_down import v_project
from src.polytope_visualizer.rotate import v_rotate
from src.polytope_visualizer.diagram import CoxeterDiagram


class CoxeterRenderer(tk.Frame):
    def __init__(self, root, width, height, diagram: CoxeterDiagram, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.iterations = 10

        self.diagram = diagram
        self.dimension = diagram.dimension
        self.points = diagram.polytope()

        self.width, self.height = width, height
        self.canvas = tk.Canvas(self, width=width, height=height, borderwidth=5, relief="groove")
        self.canvas.pack()

        self.scaling = 100
        self.dot_size = 20
        self.screen_dist = 300
        self.eye_dist = 600

        # Set up a zero array for the angles
        self.angles = [0] * 3

    def draw(self):
        """Renders the diagram's polytope"""
        self.canvas.delete('all')

        rotated_points = v_rotate(self.points * self.scaling, float(self.angles[0]), 0, 1, self.dimension)
        rotated_points = v_rotate(rotated_points, float(self.angles[1]), 0, 2, self.dimension)
        rotated_points = v_rotate(rotated_points, float(self.angles[2]), 1, 2, self.dimension)

        proj_points = np.copy(rotated_points)
        while proj_points.shape[1] != 2:
            proj_points, heights = v_project(proj_points, self.screen_dist, self.eye_dist)

        heights = np.reshape(heights, (-1, 1))
        heights *= self.dot_size

        points_and_heights = np.concatenate((proj_points, heights), axis=1)

        # Sort points based on distance to camera
        indices = np.argsort(heights, axis=0)
        sorted_points_and_heights = np.take_along_axis(points_and_heights, indices, axis=0)

        for p in sorted_points_and_heights:
            self.canvas.create_oval(p[0] - p[2] + self.width / 2, p[1] - p[2] + self.height / 2,
                                    p[0] + p[2] + self.width / 2, p[1] + p[2] + self.height / 2,
                                    fill="white")

        self.canvas.after(1000 // 60, self.draw)

    def set_diagram(self, diagram: CoxeterDiagram):
        self.diagram = diagram
        self.dimension = diagram.dimension
        self.points = diagram.polytope()

    def update_angle(self, index, value):
        self.angles[index] = float(value) * math.pi / 180

    def set_scale(self, scale: str):
        self.scaling = float(scale)

    def set_dot_size(self, size: str):
        self.dot_size = float(size)

    def set_screen_dist(self, dist: str):
        self.screen_dist = float(dist)

    def set_eye_dist(self, dist: str):
        self.eye_dist = float(dist)
