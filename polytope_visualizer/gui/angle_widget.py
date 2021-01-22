from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QSlider, QPushButton, QSpinBox, QLabel
from PyQt5.QtCore import Qt
from functools import partial
from .slider import LabelledSlider
from ..math.rotate import Rotor
import math


class AngleWidget(QWidget):
    rotorsChanged = QtCore.pyqtSignal(list)
    angleChanged = QtCore.pyqtSignal(list)

    def __init__(self):
        super().__init__()

        self.rotor_widgets = []

        add = QPushButton("Add rotation")
        add.clicked.connect(self.add_rotor)

        self.layout = QtWidgets.QVBoxLayout()
        buttons = QtWidgets.QHBoxLayout()
        buttons.addWidget(add)

        self.layout.addLayout(buttons)

        self.setLayout(self.layout)

    def add_rotor(self):
        widget = RotorWidget()
        widget.deleted.connect(self.remove_rotor)
        widget.changed.connect(self.update_rotors)
        self.rotor_widgets.append(widget)
        self.layout.addWidget(widget)

    def remove_rotor(self, widget):
        self.rotor_widgets.remove(widget)
        widget.deleteLater()
        self.update_rotors()

    def rotors(self):
        rotors = []
        for widget in self.rotor_widgets:
            rotors.append(widget.rotor)
        return rotors

    def update_rotors(self):
        self.rotorsChanged.emit(self.rotors())


class RotorWidget(QWidget):
    deleted = QtCore.pyqtSignal(object)
    changed = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.rotor = Rotor(0, 1, 0.0)

        layout = QtWidgets.QHBoxLayout()

        axis1 = QSpinBox()
        axis1.valueChanged.connect(self.set_axis1)
        axis2 = QSpinBox()
        axis2.valueChanged.connect(self.set_axis2)

        angle_slider = QSlider(Qt.Horizontal)
        angle_slider.valueChanged.connect(self.set_angle)
        angle_slider.setMaximum(360)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete)

        layout.addWidget(axis1)
        layout.addWidget(axis2)
        layout.addWidget(angle_slider)
        layout.addWidget(delete_button)
        self.setLayout(layout)

    def set_axis1(self, value):
        self.rotor.axes[0] = value
        self.changed.emit()

    def set_axis2(self, value):
        self.rotor.axes[1] = value
        self.changed.emit()

    def set_angle(self, value):
        self.rotor.angle = value * math.pi / 180
        self.changed.emit()

    def delete(self):
        self.deleted.emit(self)
