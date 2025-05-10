# -*- coding: utf-8 -*-
from icecream import ic

def get_params():
    return [1., 1.]


def predict(params, x, y):
    a, b = params
    ic(a, b)
    ic(a * x + b)
    return a * x + b

def residual(params, x, y):
    ic(x, y)
    pred = predict(params, x, y)
    ic(y - pred)
    return y - pred
