from PyQt5.QtWidgets import QWidget, QHBoxLayout

from src.polytope_visualizer.math.diagram import CoxeterDiagram
from .polytope_renderer import Renderer
from .diagram_editor import DiagramEditor


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.diagram_editor = DiagramEditor()
        self.renderer = Renderer(self.diagram_editor.diagram())

        self.diagram_editor.diagramConfirmed.connect(self.renderer.set_diagram)

        layout = QHBoxLayout()
        layout.addWidget(self.renderer)
        layout.addWidget(self.diagram_editor)

        self.setLayout(layout)
