import numpy as np
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from .model import get_models

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("doodlebug")
        self.points = []

        # Example dictionary
        self.option_dict = get_models()
        self.selected_option = None

        # Matplotlib figure
        self.canvas = FigureCanvas(plt.Figure())
        self.ax = self.canvas.figure.subplots()
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.ax.set_title("Left-click: add point, Right-click: remove nearest point")

        # Reset button
        self.reset_button = QPushButton("Reset Points")
        self.reset_button.clicked.connect(self.reset_points)

        # Dropdown (ComboBox) for selecting option
        self.dropdown = QComboBox()
        self.dropdown.addItems(self.option_dict.keys())
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

    def on_click(self, event):
        if event.inaxes:
            x, y = event.xdata, event.ydata

            if event.button == 1:  # Left-click → add point
                self.points.append((x, y))
                print(f"Added point: ({x:.2f}, {y:.2f})")

            elif event.button == 3:  # Right-click → remove nearest point
                self.remove_nearest_point(x, y)

            self.redraw_points()

    def remove_nearest_point(self, x, y, threshold=0.5):
        if not self.points:
            return

        points_array = np.array(self.points)
        distances = np.sqrt((points_array[:, 0] - x)**2 + (points_array[:, 1] - y)**2)
        min_idx = np.argmin(distances)
        min_dist = distances[min_idx]

        if min_dist < threshold:
            removed_point = self.points.pop(min_idx)
            print(f"Removed point: ({removed_point[0]:.2f}, {removed_point[1]:.2f})")
        else:
            print(f"No point near ({x:.2f}, {y:.2f}) to remove (min dist = {min_dist:.2f})")

    def redraw_points(self):
        self.ax.cla()
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.ax.set_title("Left-click: add point, Right-click: remove nearest point")

        if self.points:
            points_array = np.array(self.points)
            self.ax.plot(points_array[:, 0], points_array[:, 1], 'ro')

        self.canvas.draw()

    def reset_points(self):
        self.points.clear()
        self.redraw_points()
        print("All points cleared.")

    def option_changed(self, text):
        self.selected_option = text
        print(f"Selected option: {text} → {self.option_dict[text]}")
