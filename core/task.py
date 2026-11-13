import pathlib
from typing import Literal, Union

import numpy as np

from rewardgym import check_random_state
from rewardgym.reward_classes import DriftingReward
from rewardgym.tasks.yaml_tools import load_task_from_yaml


def get_task(
    render_backend: Literal["pygame", "psychopy"] = None,
    random_state: Union[int, np.random.Generator] = 1000,
    key_dict=None,
    **kwargs,
):
    random_state = check_random_state(random_state)
    yaml_file = pathlib.Path(__file__).parents[1].resolve() / "task.yaml"
    info_dict, environment_graph = load_task_from_yaml(yaml_file)

    environment_graph = {
        0: ([1, 2], 0.7),
        1: [3, 4],
        2: [5, 6],
        3: [],
        4: [],
        5: [],
        6: [],
    }

    reward_structure = {
        3: DriftingReward(random_state=random_state, p=None),
        4: DriftingReward(random_state=random_state, p=None),
        5: DriftingReward(random_state=random_state, p=None),
        6: DriftingReward(random_state=random_state, p=None),
    }

    action_map = {}

    if render_backend is not None:
        from .render import get_render_info

        if key_dict is None:
            key_dict = {"left": 0, "right": 1}

        render_dict, _ = get_render_info(
            random_state=random_state, key_dict=key_dict, fullpoints=info_dict["meta"]["fullpoints"]
        )
        info_dict.update(render_dict)

    return environment_graph, reward_structure, info_dict
