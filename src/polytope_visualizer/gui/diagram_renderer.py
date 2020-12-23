from typing import Optional

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QFrame, QSlider, QGridLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter
from ..math.diagram import CoxeterDiagram


class DiagramRenderer(QFrame):
    """Frame for rendering a Coxeter diagram"""
    node_spacing = 40
    node_radius = 5
    node_ring_radius = 9

    def __init__(self):
        super().__init__()
        self.diagram: Optional[CoxeterDiagram] = None

        self.setMinimumSize(200, 100)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_diagram(qp)
        qp.end()

    def draw_diagram(self, qp):
        if self.diagram is None:
            return

        for idx, node in enumerate(self.diagram.nodes):
            qp.setBrush(Qt.black)
            qp.drawEllipse(QPoint((idx + 1) * self.node_spacing, 50),
                           self.node_radius, self.node_radius)
            qp.setBrush(Qt.NoBrush)

            if node:
                qp.drawEllipse(QPoint((idx + 1) * self.node_spacing, 50),
                               self.node_ring_radius, self.node_ring_radius)

        qp.drawLine(self.node_spacing, 50,
                    self.node_spacing + self.node_spacing * (len(self.diagram.nodes) - 1), 50)

        # Draw edge numbers
        for idx, edge in enumerate(self.diagram.edges):
            # Blank edges are implicit 3s
            if edge != 3:
                left_edge = self.node_spacing + self.node_spacing * idx
                right_edge = self.node_spacing + self.node_spacing * (idx + 1)
                top_edge = 30
                bottom_edge = 48

                qp.drawText(left_edge, top_edge, right_edge-left_edge, bottom_edge-top_edge,
                            Qt.AlignCenter, str(edge))


    def set_diagram(self, diagram: CoxeterDiagram):
        self.diagram = diagram
        self.update()