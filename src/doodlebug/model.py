# -*- coding: utf-8 -*-
from icecream import ic
import numpy as np



def get_models():
    model_by = {
            "Linear": Linear(),
            "Curve": Curve(),
            }

    return model_by


class Linear():
    def __init__(self):
        self.name = "Linear"
        self.p = {
                "a": 1.,
                "b": 1.,
                }

    def get_model_func(self):
        return lambda x: self.p["a"] * x + self.p["b"]


class Curve():
    def __init__(self):
        self.name = "Curve"
        self.p = {
                "a": 0.1,
                "b": 1.,
                "c": 1.,
                }

    def get_model_func(self):
        return lambda x: self.p["a"] * x**2 + self.p["b"] * x + self.p["c"]
