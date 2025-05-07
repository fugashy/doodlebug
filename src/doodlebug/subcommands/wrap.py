import functools
import json
import os

import click
from icecream import ic


def save_as_json(f):
    @functools.wraps(f)
    @click.pass_context
    def wrapper(ctx, *args, **kwargs):
        result = f(*args, **kwargs)


        config_filepath = ctx.obj["config_filepath"]
        config = dict()
        if os.path.exists(config_filepath):
            with open(config_filepath, "r") as fp:
                config = json.load(fp)

        ic("before")
        ic(config)

        config.update(ctx.obj)

        ic("after")
        ic(config)

        with open(config_filepath, "w") as fp:
            json.dump(config, fp, indent=2)

        ic(f"Save file to {config_filepath}")

        return result

    return wrapper
