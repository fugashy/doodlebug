from icecream import ic
import json


from .model import create as create_model


def optimize(config_by):
    ic("Optimization")

    with open(config_by["config_filepath"], "r") as f:
        config = json.load(f)

    ic(config)

    model = create_model(config["model"])
