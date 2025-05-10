import numpy as np
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from .model import get_models
from .point_manager import PointManager
from .optimize import optimize


def _init_ax(ax, x_min=0., x_max=10., y_min=0., y_max=10.):
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_title("Left-click: add point, Right-click: remove nearest point")


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("doodlebug")
        self.point_manager = PointManager()


        # Matplotlib figure
        self.canvas = FigureCanvas(plt.Figure())
        self.ax = self.canvas.figure.subplots()
        _init_ax(self.ax)

        # Reset button
        self.reset_button = QPushButton("Reset Points")
        self.reset_button.clicked.connect(self.reset_points)

        # Dropdown (ComboBox) for selecting option
        self.dropdown = QComboBox()
        self.dropdown.addItems(get_models().keys())
        self.dropdown.currentTextChanged.connect(self.option_changed)

        # Model
        self.selected_option = list(get_models().keys())[0]
        self.model = get_models()[self.selected_option]

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
        self.redraw()

        self.selected_option = text
        self.model = get_models()[self.selected_option]
        print(f"→ {self.selected_option}")

    def redraw(self):
        self.ax.cla()
        _init_ax(self.ax)

        if not self.point_manager.get():
            self.canvas.draw()
            return

        # Plot observed points
        points_array = np.array(self.point_manager.get())
        self.ax.plot(points_array[:,0], points_array[:,1], 'ro')

        # Plot a optimized line
        optimize(points_array, self.model)
        self.model.plot(self.ax, points_array[:,0], points_array[:,1])

        self.canvas.draw()
