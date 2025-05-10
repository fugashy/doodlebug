# -*- coding: utf-8 -*-
def get_params():
    return [1., 1., 1.]


def predict(params, x, y):
    a, b, c = params
    return a * x**2 + b * x + c


def residual(params, x, y):
    pred = predict(params, x, y)
    return y - pred
