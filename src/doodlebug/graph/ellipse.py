# -*- coding: utf-8 -*-
def get_params():
    return [1., 1., 1., 1.]

def predict(params, x, y):
    cx, cy, rx, ry = params
    return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2


def residual(params, x, y):
    pred = predict(params, x, y)
    return 1 - pred
