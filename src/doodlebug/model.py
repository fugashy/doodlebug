# -*- coding: utf-8 -*-
from icecream import ic
import numpy as np



def get_models():
    model_by = {
            "linear": Linear,
            "michaelis_menten_equation": MichaelisMentenEquation,
            }

    return model_by


class Linear():
    def __init__(self):
        self.name = "Linear"
        self.param_by = {
                "a": 1.,
                "b": 1.,
                }


class MichaelisMentenEquation():
    def __init__(self):
        self.name = "MichaelisMentenEquation"
        self.param_by = {
                "b0": 1.,
                "b1": 1.,
                }
