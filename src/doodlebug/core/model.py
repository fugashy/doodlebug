# -*- coding: utf-8 -*-
from icecream import ic
import numpy as np



def create(config):
    ic(config)

    model_by = {
            "linear": Linear,
            }

    return model_by[config["type"]].create(config["params"])



class Model(object):
    def __init__(self, p, expected_dof):
        u"""
        Args:
            p: パラメータ(list of float)
            expected_dof: 期待するdof(int)
        """
        if type(p) is not list:
            raise Exception('Parameter should be formed as list')

        if type(p[0]) is not float:
            raise Exception('Parameter type should be float')

        if len(p) != expected_dof:
            raise Exception(
                    'Order of parameter({}) is invalid'.format(len(p)))

        # パラメータ
        self._p = np.array(p)
        # モデル式
        self._f = lambda x, p: np.inf
        # 残差式
        self._r = lambda x, p: np.inf
        # 残差勾配
        self._rg = lambda x, p: [np.inf]
        # モデル式のx0におけるテイラー展開
        self._tf = [lambda x, x0, p: np.inf]

    def fx(self, x):
        return self._f(x, self._p)

    def update(self, p):
        if len(p) != len(self._p):
            print('Invalid dof({}). We ignore this updation.'.format(len(p)))
            return
        self._p = p

    def get_param(self):
        return deepcopy(self._p)

    def residual(self, x):
        return self._r(x, self._p)

    def residual_gradient(self, x):
        return self._rg(x, self._p)

    def taylor(self, x, x0):
        return \
            [
                self._tf[order](x, x0, self._p)
                for order in range(len(self._tf))
            ]

    def taylor_num(self):
        return len(self._tf)


class Linear(Model):
    @staticmethod
    def create(p):
        return Linear([p["a"], p["b"]])

    def __init__(self, p):
        super(Linear, self).__init__(p, 2)
        self._f = lambda x, p: p[0]*x[0] + p[1]
        self._r = lambda x, p: x[1] - self._f(x, p)
        drda = lambda x, p: -x[0]
        drdb = lambda x, p: -1.0
        self._rg = lambda x, p: [drda(x, p), drdb(x, p)]

        self._tf[0] = lambda x, x0, p: self._f(x0, p) + p[0] * (x[0] - x0[0])
        self._tf.append(lambda x, x0, p: self._tf[0](x, x0, p))
