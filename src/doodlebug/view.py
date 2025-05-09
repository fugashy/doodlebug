import numpy as np
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from .model import get_models
from .point_manager import PointManager


def _init_ax(ax):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_title("Left-click: add point, Right-click: remove nearest point")


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("doodlebug")
        self.point_manager = PointManager()

        # Example dictionary
        self.model_by = get_models()
        self.selected_option = list(self.model_by.keys())[0]

        # Matplotlib figure
        self.canvas = FigureCanvas(plt.Figure())
        self.ax = self.canvas.figure.subplots()
        _init_ax(self.ax)

        # Reset button
        self.reset_button = QPushButton("Reset Points")
        self.reset_button.clicked.connect(self.reset_points)

        # Dropdown (ComboBox) for selecting option
        self.dropdown = QComboBox()
        self.dropdown.addItems(self.model_by.keys())
        self.dropdown.currentTextChanged.connect(self.option_changed)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.dropdown)
        layout.addWidget(self.reset_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connect click event
        self.canvas.mpl_connect("button_press_event", self.on_click)

        self.redraw()

    def on_click(self, event):
        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata

        if event.button == 1:  # Left-click → add point
            self.point_manager.add(x, y)
            print(f"Added point: ({x:.2f}, {y:.2f})")

        elif event.button == 3:  # Right-click → remove nearest point
            self.point_manager.remove(x, y)

        self.redraw()

    def reset_points(self):
        self.point_manager.reset()
        self.redraw()
        print("All points cleared.")

    def option_changed(self, text):
        self.point_manager.reset()
        self.redraw()

        self.selected_option = text
        print(f"→ {self.selected_option}")

    def redraw(self):
        self.ax.cla()
        _init_ax(self.ax)

        if not self.point_manager.get():
            self.canvas.draw()
            return

        points_array = np.array(self.point_manager.get())
        self.ax.plot(points_array[:, 0], points_array[:, 1], 'ro')

        model = get_models()[self.selected_option]
        x_range = (
                min(points_array[:,0]),
                max(points_array[:,0]))
        model_func = model.get_model_func()
        ys = model_func(points_array[:,0])
        self.ax.plot(points_array[:,0], ys, "g--", label="Model")

        self.canvas.draw()
