from icecream import ic
import json


def optimize(config_by):
    ic("Optimization")

    with open(config_by["config_filepath"], "r") as f:
        config = json.load(f)

    ic(config)
