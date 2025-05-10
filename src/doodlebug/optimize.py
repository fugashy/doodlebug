# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import least_squares


def optimize(data, model):
    res = least_squares(
            model.residual,
            model.params,
            args=(data[:,0], data[:,1]))
    model.params = res.x

