from icecream import ic
import g2opy as g2o
import numpy as np


def nx2g2o(nx_graph) -> g2o.SparseOptimizer:
    optimizer = g2o.SparseOptimizer()
    solver = g2o.BlockSolverSE2(g2o.LinearSolverDenseSE2())
    algorithm = g2o.OptimizationAlgorithmLevenberg(solver)
    optimizer.set_algorithm(algorithm)

    node_conf_by = {
            "fixed": {
                "sensor": False,
                "obs": False,
                "ref": True,
                },
            "info_mat": {
                "sensor": np.eye(3) * 10000.,
                "obs": np.eye(3),
                }
            }
    node_id_by = dict()

    ic.disable()
    for i, (id_, attr) in enumerate(nx_graph.nodes(data=True)):
        ic(i, id_, attr)
        node_id_by[id_] = i

        v = g2o.VertexSE2()
        v.set_id(i)
        v.set_estimate(g2o.SE2(attr["x"], attr["y"], 0))
        v.set_fixed(node_conf_by["fixed"][attr["type"]])

        optimizer.add_vertex(v)

    ic(node_id_by)

    for src, dst, attr in nx_graph.edges(data=True):
        ic(src, dst, attr)

        e = g2o.EdgeSE2()

        e.set_vertex(0, optimizer.vertex(node_id_by[src]))
        e.set_vertex(1, optimizer.vertex(node_id_by[dst]))

        src_node = ic(nx_graph.nodes[src])
        dst_node = ic(nx_graph.nodes[dst])
        sp = np.array([src_node["x"], src_node["y"]])
        dp = np.array([dst_node["x"], dst_node["y"]])
        mp = ic(dp - sp)
        e.set_measurement(g2o.SE2(mp[0], mp[1], 0))

        try:
            e.set_information(node_conf_by["info_mat"][src_node["type"]])
        except KeyError:
            continue

        optimizer.add_edge(e)
    ic.enable()

    return optimizer, node_id_by


def g2o2nx(optimizer, node_id_by, graph_before):
    for g2o_node_id in optimizer.vertices():
        # 対応するnxのノードIDを得る
        nx_node_id = None
        for nid, gid in node_id_by.items():
            if g2o_node_id == gid:
                nx_node_id = nid
                break
        if nx_node_id is None:
            ic("something went wrong")
            return None

        v = optimizer.vertex(g2o_node_id)
        e = v.estimate()

        target_node = graph_before.nodes[nx_node_id]
        ic(target_node)
        target_node["x"] = e.translation()[0]
        target_node["y"] = e.translation()[1]
        ic(target_node)

    return graph_before
