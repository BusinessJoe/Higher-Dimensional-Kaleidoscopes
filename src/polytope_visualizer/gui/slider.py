from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QVBoxLayout
from PyQt5 import QtCore
import sys


class LabelledSlider(QWidget):
    def __init__(self, label, *args, **kwargs):
        super().__init__()
        layout = QVBoxLayout()

        self.label = QLabel(text=label)
        self.sl = QSlider(*args, **kwargs)

        layout.addWidget(self.label)
        layout.addWidget(self.sl)

        self.setLayout(layout)