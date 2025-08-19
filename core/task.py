import pathlib
from typing import Literal, Union

import numpy as np

try:
    from ....reward_classes import DriftingReward
    from ....utils import check_random_state
    from ...yaml_tools import load_task_from_yaml
except ImportError:
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

    if render_backend == "pygame":
        from .backend_pygame import get_pygame_info

        pygame_dict = get_pygame_info(action_map)
        info_dict.update(pygame_dict)

    elif render_backend == "psychopy" or render_backend == "psychopy-simulate":
        from .backend_psychopy import get_psychopy_info

        if key_dict is None:
            key_dict = {"left": 0, "right": 1}

        psychopy_dict, _ = get_psychopy_info(
            random_state=random_state, key_dict=key_dict, fullpoints=info_dict["meta"]["fullpoints"]
        )
        info_dict.update(psychopy_dict)

    return environment_graph, reward_structure, info_dict
