import json
from copy import deepcopy
import pickle

from icecream import ic
import numpy as np
import numpy.linalg as LA
import networkx as nx
import g2opy as g2o

from .model import create as create_model
from .updater import create as create_updater
from .optimize_utils import (
        nx2g2o,
        g2o2nx,
        )


def optimize(config_by):
    ic("Optimization")

    with open(config_by["config_filepath"], "r") as f:
        config = json.load(f)

    ic(config)

    model = create_model(config["model"])
    updater = create_updater(config["updater"])


class Optimizer():
    def __init__(self, model, updater, tolerance):
        u"""
        コンストラクタ
        Args:
            model: データが従っているとされるモデル(models)
            update_func: パラメータを更新する関数(update_functions)
            tolerance: 最適化が完了したと判断するしきい値(float)
        Returns:
            なし
        """
        self.__model = model
        self.__updater = updater
        self.__tolerance = tolerance
        self.__num_iteration = 0


    def optimize(self, data, once=False):
        u"""
        更新ベクトルのノルムが一定値になるまでパラメータの更新を行う

        Args:
            data: 観測データ
            once: 一度で止める(bool)

        Returns:
            更新回数(int)
        """
        try:
            while True:
                delta = self.__updater.update(
                        deepcopy(self.__model), data)

                # 更新量が十分小さくなったら終了
                delta_norm = LA.norm(delta, ord=2)
                if delta_norm < self.__tolerance:
                    break

                # 更新
                param = np.array(self.__model.get_param())
                param -= delta
                self.__model.update(param)

                self.__num_iteration += 1
                if once:
                    break
        except KeyboardInterrupt:
            print('user interruption has occured')
        finally:
            return self.__num_iteration


def optimize_graph(graph_filepath):
    ic(graph_filepath)

    with open(graph_filepath, "rb") as f:
        graph_before = pickle.load(f)

    ic(graph_before)

    optimizer, g2o_node_id_by = nx2g2o(graph_before)
    optimizer.initialize_optimization()
    optimizer.optimize(10)

    graph_after = g2o2nx(optimizer, g2o_node_id_by, graph_before)

    output_graph_path = f"{graph_filepath}-after.gpickle"
    with open(output_graph_path, "wb") as f:
        pickle.dump(graph_after, f)

    ic("done")
    ic(f"output the graph optimized: {output_graph_path}")




