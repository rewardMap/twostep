try:
    from rewardgym.utils import check_seed
except ImportError:
    from ....utils import check_seed


def get_configs(stimulus_set: str = "1"):
    check_seed(int(stimulus_set))

    config = {
        "name": "risk-sensitive",
        "stimulus_set": stimulus_set,
        "isi": [],
        "iti": [],
        "condition": [],
        "condition_dict": {},
        "ntrials": 1,
        "update": [],
        "add_remainder": True,
        "breakpoints": [],
        "break_duration": 0,
    }

    return config
