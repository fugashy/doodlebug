# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import least_squares


def optimize(data, model, params):
    res = least_squares(model.residual, params, args=(data[:,0], data[:,1]))

    return res.x
