try:
    from rewardgym.utils import check_random_state
    from rewardgym.tasks.utils import check_conditions_not_following
except ImportError:
    from ....utils import check_random_state
    from ...utils import check_conditions_not_following


def get_configs(stimulus_set: str = "1"):
    condition_dict = {
        "expected-transition": {0: {0: 1, 1: 2}},
        "unexpected-transition": {0: {0: 2, 1: 1}},
        None: None,
    }
    seed = check_random_state(int(stimulus_set))

    # Actually create pseudo-random transitions:
    transition_list = ["expected-transition"] * 14 + ["unexpected-transition"] * 6
    iti_jitter = [0.1, 0.15, 0.2, 0.25, 0.3] * 4

    conditions = []
    itis = []

    for _ in range(9):
        reject = True
        itis.extend(
            seed.choice(a=iti_jitter, size=len(iti_jitter), replace=False).tolist()
        )

        while reject:
            condition_proposal = seed.choice(
                a=transition_list, size=len(transition_list), replace=False
            ).tolist()
            check = check_conditions_not_following(
                condition_proposal, ["unexpected-transition"], 1
            )

            if check:
                reject = False
                conditions.extend(condition_proposal)

    configs = {
        "name": "two-step",
        "set": stimulus_set,
        "iti": itis,
        "isi": None,
        "condition": conditions,
        "condition_dict": condition_dict,
        "ntrials": len(conditions),
        "update": ["iti"],
        "add_remainder": True,
        "breakpoints": [int(len(conditions) // 2 - 1)],
        "break_duration": 45,
    }

    return configs
