from copy import deepcopy
import numpy as np
import pathlib

try:
    from ....psychopy_render import (
        TwoStimuliWithResponseAndSelection,
        FeedBackStimulus,
        ImageStimulus,
        BaseStimulus,
    )
    from ....stimuli import (
        fixation_cross,
        STIMULUS_DEFAULTS,
        generate_stimulus_properties,
        draw_spaceship,
        draw_alien,
        make_card_stimulus,
    )
    from ....utils import check_random_state

except ImportError:
    from rewardgym import check_random_state
    from rewardgym.psychopy_render import (
        TwoStimuliWithResponseAndSelection,
        FeedBackStimulus,
        ImageStimulus,
        BaseStimulus,
    )
    from rewardgym.stimuli import (
        fixation_cross,
        STIMULUS_DEFAULTS,
        generate_stimulus_properties,
        draw_spaceship,
        draw_alien,
        make_card_stimulus,
    )


def twostep_card_stimuli(random_state, stim_defaults=STIMULUS_DEFAULTS):
    random_state = check_random_state(random_state)

    stim_defaults = deepcopy(stim_defaults)
    colors = stim_defaults["colors"]
    set_colors = random_state.choice(np.arange(len(colors[:-1])), 3, replace=False)

    stim_set = {}
    stim_properties = {}
    for n in range(3):
        stim_set[n] = []

        stimulus_properties = []
        for _ in range(2):
            st_p = generate_stimulus_properties(
                random_state=random_state,
                colors=[tuple(colors[set_colors[n]])] * 4,
                patterns=[(1, 1), (2, 2)],
                shapes=stim_defaults["shapes"],
            )
            stimulus_properties.append(st_p)
            stim_defaults["shapes"] = [
                i for i in stim_defaults["shapes"] if i != st_p["shapes"]
            ]

        height = 375 if n == 0 else 250
        stim_properties[n] = stimulus_properties
        stim_set[n] = [
            make_card_stimulus(stim_properties[n][k], width=250, height=height)
            for k in range(2)
        ]

    return stim_set, stim_properties


def twostep_alien_stimuli(random_state, stim_defaults=STIMULUS_DEFAULTS):
    random_state = check_random_state(random_state)

    stim_defaults = deepcopy(stim_defaults)
    colors = stim_defaults["colors"]
    set_colors = random_state.choice(np.arange(len(colors[:-1])), 3, replace=False)
    set_colors = [colors[i] for i in set_colors]
    alien_order = random_state.choice(np.arange(4), 4, replace=False)
    space_order = random_state.choice(np.arange(2), 2, replace=False)

    stim_set = {}

    stim_set[0] = [
        draw_spaceship(
            version=space_order[0], height=400, width=400, body_color=set_colors[0]
        ),
        draw_spaceship(
            version=space_order[1], height=400, width=400, body_color=set_colors[0]
        ),
    ]

    stim_set[1] = [
        draw_alien(
            version=alien_order[0], height=300, width=300, body_color=set_colors[1]
        ),
        draw_alien(
            version=alien_order[1], height=300, width=300, body_color=set_colors[1]
        ),
    ]

    stim_set[2] = [
        draw_alien(
            version=alien_order[2], height=300, width=300, body_color=set_colors[2]
        ),
        draw_alien(
            version=alien_order[3], height=300, width=300, body_color=set_colors[2]
        ),
    ]

    stim_properties = {}
    return stim_set, stim_properties


def two_step_alien_images(random_state, directory=None, stim_defaults=STIMULUS_DEFAULTS):

    def recolor(input_file, new_color, target_size=(300, 300)):
        from PIL import Image

        img = Image.open(input_file).convert("RGBA")
        img.thumbnail(target_size, Image.Resampling.LANCZOS)  # keeps aspect ratio
        data = np.array(img, dtype=float)
        gray = np.array(img.convert("L"), dtype=float)  # convert to grayscale (1 channel)
        data[..., :3] = np.stack([gray]*3, axis=-1)    #

        r, g, b, a = data[..., 0], data[..., 1], data[..., 2], data[..., 3]

        # Mask: ignore transparent, black, white
        mask = (a > 0) & ~((r < 20) & (g < 20) & (b < 20)) & ~((r > 235) & (g > 235) & (b > 235))

        factors = np.array(new_color) / 255.0

        # Apply multiplicative recoloring only inside mask
        for i in range(3):
            data[..., i][mask] = data[..., i][mask] * factors[i]

        data = np.clip(data, 0, 255)

        data = data[::-1, :] / 255

        return data

    random_state = check_random_state(random_state)

    stim_defaults = deepcopy(stim_defaults)
    colors = stim_defaults["colors"]
    set_colors = random_state.choice(np.arange(len(colors[:-1])), 3, replace=False)
    set_colors = [colors[i] for i in set_colors]

    space_order = random_state.choice(np.arange(2), 2, replace=False)

    stim_set = {}

    stim_set[0] = [
        draw_spaceship(
            version=space_order[0], height=400, width=400, body_color=set_colors[0]
        ),
        draw_spaceship(
            version=space_order[1], height=400, width=400, body_color=set_colors[0]
        ),
    ]

    if directory is None:
        directory = pathlib.Path(__file__).parents[0].resolve() / "assets"/ "stimuli_svg"

    aliens = list(directory.glob("Alien*rec.png"))

    alien_order = random_state.choice(aliens, 4, replace=False)

    planets = list(directory.glob("Planets*rec.png"))

    planet_order = random_state.choice(planets, 2, replace=False)

    stim_set[1] = [
        recolor(alien_order[0].as_posix(), new_color=set_colors[1]),
        recolor(alien_order[1].as_posix(), new_color=set_colors[1]),
        recolor(planet_order[0].as_posix(), new_color=set_colors[1], target_size=(300, 300)),
        ]

    stim_set[2] = [
        recolor(alien_order[2].as_posix(), new_color=set_colors[2]),
        recolor(alien_order[3].as_posix(), new_color=set_colors[2]),
        recolor(planet_order[1].as_posix(), new_color=set_colors[2], target_size=(300, 300)),
        ]

    stim_properties = {}
    return stim_set, stim_properties


def get_psychopy_info(
    random_state=111,
    key_dict={"left": 0, "right": 1},
    external_stimuli=None,
    fullpoints=None,
    **kwargs,
):
    random_state = check_random_state(random_state)

    if external_stimuli is None:
        stim_set, stimuli = two_step_alien_images(random_state)
    else:
        stim_set, stimuli = external_stimuli

    reward_feedback = FeedBackStimulus(
        1.0,
        text="{0}",
        target="reward",
        name="reward",
        bar_total=fullpoints,
        rl_label="reward"
    )

    fix = ImageStimulus(
        image_paths=[fixation_cross()],
        duration=0.1,
        autodraw=True,
        name="initial-fixation",
    )
    fix_iti = BaseStimulus(duration=1.0, name="iti", rl_label='obs')

    fix2 = ImageStimulus(
        image_paths=[fixation_cross()],
        duration=0.25,
        autodraw=True,
        name="transition",
    )

    image_shift = 325

    final_step = [reward_feedback, fix_iti]

    def first_state(stim1, stim2, key_dict):
        tmp_list = [
            fix,
            TwoStimuliWithResponseAndSelection(
                duration=2.0,
                key_dict=key_dict,
                name_phase1="stage-1-decision",
                duration_phase1=0.1,
                name_phase2="stage-1-selection",
                duration_phase2=0.75,
                images=[stim1, stim2],
                positions=[(-image_shift, 0), (image_shift, 0)],
                rl_label="action",
                rl_label_phase1="obs",
                rl_label_phase2='reward',
            ),
        ]

        return tmp_list

    def second_state(s2_img1, s2_img2, s2_planet, key_dict):
        tmp_list = [
            fix2,
            ImageStimulus(
                image_paths=[s2_planet, fixation_cross()],
                duration=0.25,
                name="planet",
                positions=[(0, -100), (0, 0)]
            ),
            TwoStimuliWithResponseAndSelection(
                duration=2.0,
                key_dict=key_dict,
                name_phase1="stage-2-decision",
                duration_phase1=0.1,
                name_phase2="stage-2-selection",
                duration_phase2=0.5,
                images=[s2_img1, s2_img2, s2_planet, fixation_cross()],
                positions=[(-image_shift, 0), (image_shift, 0), (0, -100), (0, 0)],
                rl_label="action",
                rl_label_phase1="obs",
                flip_probability=0.5,
            ),
        ]

        return tmp_list

    info_dict = {
        0: {
            "psychopy": first_state(
                stim1=stim_set[0][0], stim2=stim_set[0][1], key_dict=key_dict
            )
        },
        1: {
            "psychopy": second_state(
                s2_img1=stim_set[1][0],
                s2_img2=stim_set[1][1],
                s2_planet=stim_set[1][2],
                key_dict=key_dict,
            )
        },
        2: {
            "psychopy": second_state(
                s2_img1=stim_set[2][0],
                s2_img2=stim_set[2][1],
                s2_planet=stim_set[2][2],
                key_dict=key_dict,
            )
        },
        3: {"psychopy": final_step},
        4: {"psychopy": final_step},
        5: {"psychopy": final_step},
        6: {"psychopy": final_step},
    }

    return info_dict, stimuli
