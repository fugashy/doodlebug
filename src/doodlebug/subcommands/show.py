import pickle

import click
import matplotlib.pyplot as plt
import networkx as nx


@click.group()
@click.pass_context
def show(ctx):
    pass


@show.command()
@click.argument("graph_filepath", type=str)
@click.pass_context
def graph(ctx, graph_filepath):
    with open(graph_filepath, "rb") as f:
        G = pickle.load(f)

    pose_by = dict()
    for id_, node in G.nodes(data=True):
        pose_by[id_] = (node["x"], node["y"])

    plt.figure()

    nx.draw(
            G,
            pose_by,
            node_color=[G.nodes[n]["color"] for n in G.nodes],
            node_size=[G.nodes[n]["size"] for n in G.nodes],
            edge_color=[G.edges[n]["color"] for n in G.edges])
    plt.axis("equal")

    plt.show()
