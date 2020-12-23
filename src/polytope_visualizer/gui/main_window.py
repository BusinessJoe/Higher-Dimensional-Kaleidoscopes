from PyQt5.QtWidgets import QWidget, QHBoxLayout

from ..diagram import CoxeterDiagram
from .polytope_renderer import Renderer
from .diagram_editor import DiagramEditor


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.renderer = Renderer(CoxeterDiagram([True, False, False], [3, 5]))
        self.diagram_editor = DiagramEditor()

        self.diagram_editor.diagramConfirmed.connect(self.renderer.set_diagram)

        layout = QHBoxLayout()
        layout.addWidget(self.renderer)
        layout.addWidget(self.diagram_editor)

        self.setLayout(layout)
