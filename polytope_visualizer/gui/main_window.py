from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from .polytope_renderer import Renderer
from .diagram_editor import DiagramEditor
from .angle_widget import AngleWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.diagram_editor = DiagramEditor()
        self.renderer = Renderer(self.diagram_editor.diagram())

        self.diagram_editor.diagramConfirmed.connect(self.renderer.set_diagram)

        self.angle_widget = AngleWidget()
        self.angle_widget.rotorsChanged.connect(self.renderer.set_rotors)

        layout = QHBoxLayout()
        layout.addWidget(self.renderer)
        right_panel = QVBoxLayout()
        right_panel.addWidget(self.diagram_editor)
        right_panel.addWidget(self.angle_widget)
        right_panel.addStretch(1)

        layout.addLayout(right_panel)

        self.setLayout(layout)
