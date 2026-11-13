from copy import deepcopy
import numpy as np
import pathlib

from rewardgym import check_random_state

from rewardgym.stimuli import (
    fixation_cross,
    STIMULUS_DEFAULTS,
    generate_stimulus_properties,
    draw_spaceship,
    draw_alien,
    make_card_stimulus,
)

from rewardgym.render import ImageDefinition
from rewardgym.render.passive_routines import PresentationRoutine, FeedBackRoutine
from rewardgym.render.response_routines import NAFCRoutine

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


def two_step_alien_images(random_state, directory=None, stim_defaults=STIMULUS_DEFAULTS, brighten_dark=True):

    def recolor(input_file, new_color, target_size=(300, 300), brighten_dark=brighten_dark):
        from PIL import Image

        if brighten_dark:
            if np.array(new_color).mean() < 75:
                new_color = [i + 75 for i in new_color]

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
    set_colors = random_state.choice(np.arange(len(colors[:-1])), 4, replace=False)
    set_colors = [colors[i] for i in set_colors]

    space_order = random_state.choice(np.arange(2), 2, replace=False)

    stim_set = {}

    stim_set[0] = [
        draw_spaceship(
            version=space_order[0], height=400, width=400, body_color=set_colors[0]
        ),
        draw_spaceship(
            version=space_order[1], height=400, width=400, body_color=set_colors[1]
        ),
    ]

    if directory is None:
        directory = pathlib.Path(__file__).parents[0].resolve() / "assets"/ "stimuli_svg"

    aliens = list(directory.glob("Alien*rec.png"))

    alien_order = random_state.choice(aliens, 4, replace=False)

    planets = list(directory.glob("Planets*rec.png"))

    planet_order = random_state.choice(planets, 2, replace=False)

    stim_set[1] = [
        recolor(alien_order[0].as_posix(), new_color=set_colors[2]),
        recolor(alien_order[1].as_posix(), new_color=set_colors[2]),
        recolor(planet_order[0].as_posix(), new_color=set_colors[2], target_size=(300, 300)),
        ]

    stim_set[2] = [
        recolor(alien_order[2].as_posix(), new_color=set_colors[3]),
        recolor(alien_order[3].as_posix(), new_color=set_colors[3]),
        recolor(planet_order[1].as_posix(), new_color=set_colors[3], target_size=(300, 300)),
        ]

    stim_properties = {"aliens": [i.as_posix().split('twostep')[-1] for i in alien_order],
                       "planets": [i.as_posix().split('twostep')[-1] for i in planet_order]}
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

    reward_feedback = FeedBackRoutine(
        duration=1.0, name="reward", bar_total=fullpoints, rl_label="reward"
    )

    fix = PresentationRoutine(
            stimulus_definitions=[ImageDefinition(image=fixation_cross(), name="fixation", autoDraw=True)], duration=0.1, name="initial-fixation"
        )

    fix_iti = PresentationRoutine(duration=1.0, name="iti", rl_label='obs')

    fix2 = PresentationRoutine(
            stimulus_definitions=[ImageDefinition(image=fixation_cross(), name="fixation", autoDraw=True)], duration=0.25, name="transition"
        )

    image_shift = 325

    final_step = [reward_feedback, fix_iti]

    def first_state(stim1, stim2, key_dict):
        stim1 = ImageDefinition(
            name="stim1",
            autoDraw=False,
            image=stim1
        )
        stim2 = ImageDefinition(
            name="stim2",
            autoDraw=False,
            image=stim2
        )

        tmp_list = [
            fix,
            NAFCRoutine(
                duration=2.0,
                key_dict=key_dict,
                presentation_settings={
                    "name_before": "stage-1-decision",
                    "name_after": "stage-2-selection",
                    "rl_label_before": "obs",
                    "rl_label_after": "reward",
                    "duration_after": 0.75,
                    "present_after": True,
                },
                stimulus_mapping={0: stim1, 1: stim2},
                positions={0: (-image_shift, 0), 1: (image_shift, 0)},
                name="response",
                rl_label="action",
                randomize_positions=True,
                highlight_selected=True,
            ),
        ]

        return tmp_list

    def second_state(s2_img1, s2_img2, s2_planet, key_dict):
        stim1 = ImageDefinition(
            name="s2_img1",
            autoDraw=False,
            image=s2_img1
        )
        stim2 = ImageDefinition(
            name="s2_img2",
            autoDraw=False,
            image=s2_img2
        )
        planet=ImageDefinition(
                        name="planet",
                        image=s2_planet,
                        pos=(0, -100)
                    )

        fixation=ImageDefinition(
                        name="fixation",
                        image=fixation_cross(),
                        pos=(0, 0)
                    )

        tmp_list = [
            fix2,
            PresentationRoutine(
                stimulus_definitions=[
                    planet, fixation
                ],
                name="planet",
                duration=0.25
            ),

            NAFCRoutine(
                duration=2.0,
                key_dict=key_dict,
                presentation_settings={
                    "name_before": "stage-2-decision",
                    "name_after": "stage-2-selection",
                    "rl_label_before": "obs",
                    "duration_after": 0.75,
                    "present_after": True,
                },
                stimulus_mapping={0: stim1, 1: stim2},
                scene_stimuli=[planet, fixation],
                positions={0: (-image_shift, 0), 1: (image_shift, 0)},
                rl_label="action",
                name="response",
                randomize_positions=True,
                highlight_selected=True,
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
