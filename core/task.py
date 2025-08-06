import pathlib
from typing import Literal, Union

import numpy as np

try:
    from ....reward_classes import BaseReward
    from ....utils import check_seed
    from ...yaml_tools import load_task_from_yaml
except ImportError:
    from rewardgym import check_seed
    from rewardgym.reward_classes import BaseReward
    from rewardgym.tasks.yaml_tools import load_task_from_yaml


def get_task(
    render_backend: Literal["pygame", "psychopy"] = None,
    seed: Union[int, np.random.Generator] = 1000,
    key_dict=None,
    **kwargs,
):
    seed = check_seed(seed)
    yaml_file = pathlib.Path(__file__).parents[1].resolve() / "task.yaml"
    info_dict, environment_graph = load_task_from_yaml(yaml_file)

    reward_structure = {
        0: BaseReward(reward=[0], seed=seed),
    }

    action_map = {}
    reward_meaning = {
        0: "null",
    }

    info_dict.update({"condition-meaning": reward_meaning})

    if render_backend == "pygame":
        from .backend_pygame import get_pygame_info

        pygame_dict = get_pygame_info(action_map)
        info_dict.update(pygame_dict)

    elif render_backend == "psychopy" or render_backend == "psychopy-simulate":
        from .backend_psychopy import get_psychopy_info

        if key_dict is None:
            key_dict = {"left": 0, "right": 1}

        psychopy_dict, _ = get_psychopy_info(
            seed=seed, key_dict=key_dict, fullpoints=info_dict["meta"]["fullpoints"]
        )
        info_dict.update(psychopy_dict)

    return environment_graph, reward_structure, info_dict
