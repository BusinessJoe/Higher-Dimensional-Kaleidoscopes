from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QSlider, QPushButton, QSpinBox
from PyQt5.QtCore import Qt

from ..math.diagram import CoxeterDiagram


class DiagramEditor(QWidget):
    """Widget for creating/editing linear Coxeter diagrams.

    The widget provides two signals: diagramChanged and diagramConfirmed, which both emit
    a CoxeterDiagram object.
     - diagramChanged is emitted whenever any values are changed.
     - diagramConfirmed is emitted only when the confirm button is clicked.
     """
    diagramChanged = QtCore.pyqtSignal(CoxeterDiagram)
    diagramConfirmed = QtCore.pyqtSignal(CoxeterDiagram)

    def __init__(self):
        super().__init__()

        self.length = 3
        self.node_widgets = []
        self.angle_widgets = []

        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()
        self.button_layout = QtWidgets.QHBoxLayout()

        # Slider for diagram length
        self.sl = QtWidgets.QSlider(Qt.Horizontal)
        self.sl.setMinimum(2)
        self.sl.setMaximum(6)
        self.sl.setValue(3)
        self.sl.setTickPosition(QSlider.TicksBelow)
        self.sl.setTickInterval(1)
        self.sl.valueChanged.connect(self.set_length)

        layout.addWidget(self.sl)
        layout.addLayout(self.button_layout)

        for i in range(self.length - 1):
            self.add_node_widget()
            self.add_angle_widget()
        self.add_node_widget()

        confirm = QPushButton("Confirm")
        confirm.clicked.connect(lambda: self.diagramConfirmed.emit(self.diagram()))
        layout.addWidget(confirm)

        layout.addStretch(1)

        self.setLayout(layout)

    def set_length(self, new_length):
        while len(self.node_widgets) < new_length:
            self.add_angle_widget()
            self.add_node_widget()
        while len(self.node_widgets) > new_length:
            self.remove_node_widget()
            self.remove_angle_widget()

        self.length = new_length
        self.diagramChanged.emit(self.diagram())

    def add_node_widget(self):
        toggle = QPushButton()
        toggle.setCheckable(True)
        toggle.clicked.connect(lambda: self.diagramChanged.emit(self.diagram()))
        self.node_widgets.append(toggle)
        self.button_layout.addWidget(toggle)

    def remove_node_widget(self):
        toggle = self.node_widgets.pop(-1)
        toggle.deleteLater()

    def add_angle_widget(self):
        spinbox = QSpinBox()
        spinbox.valueChanged.connect(lambda: self.diagramChanged.emit(self.diagram()))
        self.angle_widgets.append(spinbox)
        self.button_layout.addWidget(spinbox)

    def remove_angle_widget(self):
        spinbox = self.angle_widgets.pop(-1)
        spinbox.deleteLater()

    def diagram(self):
        nodes = [b.isChecked() for b in self.node_widgets]
        angles = [s.value() for s in self.angle_widgets]

        return CoxeterDiagram(nodes, angles)
