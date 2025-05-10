import numpy as np


def _remove_nearest_point(points, x, y, threshold=0.5):
    if not points:
        return None

    points_array = np.array(points)
    distances = np.sqrt((points_array[:, 0] - x)**2 + (points_array[:, 1] - y)**2)
    min_idx = np.argmin(distances)
    min_dist = distances[min_idx]

    if min_dist < threshold:
        removed_point = points.pop(min_idx)
        return removed_point
    return None


class PointManager:
    def __init__(self):
        self.points = []  # [(x, y), ...]

    def add(self, x, y):
        self.points.append((x, y))
        self.points = sorted(self.points)

    def remove(self, x, y, threshold=0.5):
        _remove_nearest_point(self.points, x, y, threshold)

    def reset(self):
        self.points.clear()

    def get(self):
        return self.points
