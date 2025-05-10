# -*- coding: utf-8 -*-
from icecream import ic
import numpy as np


from .graph import line, curve, ellipse


def get_models():
    model_by = {
            "Linear": line,
            "Curve": curve,
            "Ellipse": ellipse,
            }

    return model_by
