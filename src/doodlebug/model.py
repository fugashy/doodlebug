# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from icecream import ic
import numpy as np


def get_models():
    model_by = {
            "Line": Line(1., 1.),
            "Curve": Curve(1., 1., 1.),
            "Ellipse": Ellipse(1., 1., 1., 1., 0.),
            }

    return model_by


class DrawableModelInterface():
    def __init__(self, params):
        self.params = params

    def predict(self, x, y):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def residual(params, x, y):
        raise NotImplementedError

    @abstractmethod
    def plot(self, ax, xs, ys):
        raise NotImplementedError



class Line(DrawableModelInterface):
    def __init__(self, a, b):
        super(Line, self).__init__([a, b])

    def predict(self, x, y):
        a, b = self.params
        return a * x + b

    @staticmethod
    def residual(params, x, y):
        a, b = params
        return y - (a * x + b)

    def plot(self, ax, xs, ys):
        a, b = self.params
        ax.plot(
            xs,
            [self.predict(x, y) for x, y in zip(xs, ys)],
            "g--",
            label=f"f(x) = {a:.2f} * x + {b:.2f}")


class Curve(DrawableModelInterface):
    def __init__(self, a, b, c):
        super(Curve, self).__init__([a, b, c])

    def predict(self, x, y):
        a, b, c = self.params
        return a * x**2 + b * x + c

    @staticmethod
    def residual(params, x, y):
        a, b, c = params
        return y - (a * x**2 + b * x + c)

    def plot(self, ax, xs, ys):
        a, b, c = self.params
        ax.plot(
            xs,
            [self.predict(x, y) for x, y in zip(xs, ys)],
            "g--",
            label=f"f(x) = {a:.2f} * x**2 + {b:.2f} * x + {c:.2f}")


class Ellipse(DrawableModelInterface):
    def __init__(self, xc, yc, a, b, theta):
        super(Ellipse, self).__init__([xc, yc, a, b, theta])

    def predict(self, x, y):
        xc, yc, a, b, theta  = self.params

        cos_t = np.cos(x)
        sin_t = np.sin(y)
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)

        px = xc + a * cos_t * cos_theta - b * sin_t * sin_theta
        py = yc + a * cos_t * sin_theta + b * sin_t * cos_theta

        return [px, py]

    @staticmethod
    def residual(params, x, y):
        xc, yc, a, b, theta  = params
        cos_t = np.cos(theta)
        sin_t = np.sin(theta)
        x_shift = x - xc
        y_shift = y - yc
        x_rot = cos_t * x_shift + sin_t * y_shift
        y_rot = -sin_t * x_shift + cos_t * y_shift
        return (x_rot / a)**2 + (y_rot / b)**2 - 1

    def plot(self, ax, xs, ys):
        points = np.array([
            self.predict(x, y)
            for x, y in zip(xs, ys)]).T
        ax.plot(points[0], points[1], "g--")
