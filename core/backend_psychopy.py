try:
    from ....psychopy_render import ImageStimulus
    from ....stimuli import fixation_cross
    from ....utils import check_seed

except ImportError:
    from rewardgym import check_seed
    from rewardgym.psychopy_render import ImageStimulus
    from rewardgym.stimuli import fixation_cross


def get_psychopy_info(
    seed=111,
    key_dict={"left": 0, "right": 1},
    external_stimuli=None,
    fullpoints=None,
    **kwargs,
):
    check_seed(seed)
    stimuli = {}

    fixation = ImageStimulus(
        image_paths=[fixation_cross()], duration=0.5, name=None, autodraw=True
    )

    info_dict = {
        0: {"psychopy": [fixation]},
    }

    return info_dict, stimuli
