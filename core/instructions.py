import json
import pathlib

from rewardgym.render.routines import InstructionRoutine
from rewardgym.render.stimuli import win_cross, zero_cross
from rewardgym.render.stimulus_definitions import (
    ImageDefinition,
    TextDefinition,
)
from rewardgym.utils import NameCounter

from .render import two_step_alien_images

# Instructions modeled after
# Feher da Silva, C., Lombardi, G., Edelson, M., & Hare, T. A. (2023). Rethinking model-based and model-free influences on mental effort and striatal prediction errors. Nature Human Behaviour, 7(6), 956–969. https://doi.org/10.1038/s41562-023-01573-1
# Adjusted to space travel and trading.

instructions_path = (
    pathlib.Path(__file__).parent.resolve() / "assets" / "instructions_new.json"
)
instructions = json.loads(instructions_path.read_text())


def get_instructions(instructions=instructions):
    name = NameCounter()

    stimulus_colors = {
        "colors": [
             (150, 0, 200),
             (0, 150, 200),
             (100, 150, 50),
             (200, 200, 0),
             (0, 0, 0),
        ]
    }

    stimuli, _ = two_step_alien_images(random_state=1, stim_defaults=stimulus_colors)

    part_0_0 = TextDefinition(
        name=name.name,
        text=instructions["0.0"],
        height=28,
        pos=(0, 200),
    )

    part_0 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[part_0_0]
    )
    part_1_0 = TextDefinition(
        name=name.name,
        text=instructions["1.0"],
        height=28,
        pos=(0, 200),
    )

    part_1_1 = TextDefinition(
        name=name.name,
        text=instructions["1.1"],
        height=28,
        pos=(0, -100),
    )

    size = (100, 100)
    img_planet1 = ImageDefinition(name=name.name, image=stimuli[1][2], pos=(-200, 20), size=size)
    img_planet2 = ImageDefinition(name=name.name, image=stimuli[2][2], pos=(200, 20), size=size)

    img_alien1 = ImageDefinition(name=name.name, image=stimuli[1][0], pos=(-320, -190), size=size)
    img_alien2 = ImageDefinition(name=name.name, image=stimuli[1][1], pos=(-120, -190), size=size)

    img_alien3 = ImageDefinition(name=name.name, image=stimuli[2][0], pos=(120, -190), size=size)
    img_alien4 = ImageDefinition(name=name.name, image=stimuli[2][1], pos=(320, -190), size=size)

    part_1 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[
        img_planet1,
        img_planet2,
        img_alien1,
        img_alien2,
        img_alien3,
        img_alien4,
        part_1_0,
        part_1_1])

    size= (100, 100)

    nothing = zero_cross(
        width=100, height=100, circle_radius_inner=10, circle_radius_outer=15
    )
    winning = win_cross(
        width=100, height=100, circle_radius_inner=10, circle_radius_outer=15
    )

    part_1_0 = TextDefinition(
        name=name.name,
        text=instructions["2.0"],
        height=28,
        pos=(0, 250),
    )
    part_1_1 = TextDefinition(
        name=name.name,
        text=instructions["2.1"],
        height=28,
        pos=(0, 40),
    )

    img_alien1 = ImageDefinition(name=name.name, image=stimuli[1][0], pos=(-160, 150), size=size)

    img_alien2 = ImageDefinition(name=name.name, image=stimuli[1][0], pos=(-160, -100), size=size)

    img_win = ImageDefinition(name=name.name, image=winning, pos=(0, 150), size=winning.shape[:2])
    img_lose = ImageDefinition(name=name.name, image=nothing, pos=(0, -100), size=winning.shape[:2])

    part_2 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[
        part_1_0,
        part_1_1,
        img_alien1,
        img_alien2,
        img_win,
        img_lose,
    ])

    part_3_0 = TextDefinition(
        name=name.name,
        text="\n\n".join([instructions["3.0"],instructions["3.1"],instructions["3.2"]]),
        height=28,
        pos=(0, 150),
    )

    part_3 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[
        part_3_0])

    part_4_0 = TextDefinition(
        name=name.name,
        text="\n\n".join([instructions["4.0"],instructions["4.1"],instructions["4.2"]]),
        height=28,
        pos=(0, 150),
    )

    part_4 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[part_4_0]
    )
    part_5_0 = TextDefinition(
        name=name.name,
        text=instructions["5.0"] + "\n\n" + instructions["5.1"],
        height=28,
        pos=(0, 250),
    )

    part_5_1 = TextDefinition(
        name=name.name,
        text=instructions["5.2"],
        height=28,
        pos=(-350, 100),
    )

    part_5_2 = TextDefinition(
        name=name.name,
        text=instructions["5.3"],
        height=28,
        pos=(350, 100),
    )

    size = (100, 100)
    img_space1 = ImageDefinition(name=name.name, image=stimuli[0][0], pos=(-350, -50), size=size)
    img_space2 = ImageDefinition(name=name.name, image=stimuli[0][1], pos=(350, -50), size=size)

    img_planet1 = ImageDefinition(name=name.name, image=stimuli[1][2], pos=(-350, -200), size=size)
    img_planet2 = ImageDefinition(name=name.name, image=stimuli[2][2], pos=(350, -200), size=size)

    part_5 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[
        img_space1,
        img_space2,
        img_planet1,
        img_planet2,
        part_5_0,
        part_5_1,
        part_5_2,
    ])

    part_6_0 = TextDefinition(
        name=name.name,
        text=instructions["6.0"] + "\n\n" + instructions["6.1"],
        height=28,
        pos=(0, 275),
    )

    part_6_2 = TextDefinition(
        name=name.name,
        text=instructions["6.2"],
        height=28,
        pos=(0, -250),
    )

    size = (350, 350)
    img_space1 = ImageDefinition(name=name.name, image=stimuli[0][0], pos=(-325, 0), size=size)
    img_space2 = ImageDefinition(name=name.name, image=stimuli[0][1], pos=(325, 0), size=size)

    part_6 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[
        img_space1,
        img_space2,
        part_6_0,
        part_6_2,
    ])

    part_7_0 = TextDefinition(
        name=name.name,
        text=instructions["7.0"] + "\n\n" + instructions["7.1"] + "\n\n" + instructions["7.2"],
        height=28,
        pos=(0, 250),
    )
    part_7_3 = TextDefinition(
        name=name.name,
        text=instructions["7.3"],
        height=28,
        pos=(0, -300),
    )

    size = (100, 100)
    img_space1 = ImageDefinition(name=name.name, image=stimuli[0][0], pos=(-200, 25), size=size)

    img_planet1 = ImageDefinition(name=name.name, image=stimuli[1][2], pos=(-200, -150), size=size)
    img_planet2 = ImageDefinition(name=name.name, image=stimuli[2][2], pos=(200, -150), size=size)

    arrow_text1 = TextDefinition(
        name=name.name,
        text='↓',  # Unicode down arrow
        color='white',
        height=100,
        pos=(-200, -65)
    )

    arrow_text2 = TextDefinition(
        name=name.name,
        text='↓',  # Unicode down arrow
        color='white',
        height=100,
        pos=(0, -65),
        ori=-45
    )

    x_text = TextDefinition(
        name=name.name,
        text='X',  # Unicode down arrow
        color='red',
        height=50,
        pos=(-200, -65)
    )

    part_7 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[
        img_space1,
        img_planet1,
        img_planet2,
        part_7_0,
        part_7_3,
        arrow_text1,
        arrow_text2,
        x_text,
    ])

    part_8_0 = TextDefinition(
        name=name.name,
        text=instructions["8.0"] + "\n\n" + instructions["8.1"],
        height=28,
        pos=(0, 250),
    )

    part_8_2 = TextDefinition(
        name=name.name,
        text=instructions["8.2"],
        height=28,
        pos=(0, -250),
    )

    size = (350, 350)
    img_space1 = ImageDefinition(name=name.name, image=stimuli[1][0], pos=(-325, 0), size=size)
    img_space2 = ImageDefinition(name=name.name, image=stimuli[1][1], pos=(325, 0), size=size)

    part_8 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[
        img_space1,
        img_space2,
        part_8_0,
        part_8_2,
    ])


    part_9_0 = TextDefinition(
        name=name.name,
        text=instructions["9.0"] + "\n\n" + instructions["9.1"],
        height=28,
        pos=(0, 250),
    )

    size = (350, 350)
    img_space1 = ImageDefinition(name=name.name, image=stimuli[1][0], pos=(325, 0), size=size)
    img_space2 = ImageDefinition(name=name.name, image=stimuli[1][1], pos=(-325, 0), size=size)

    part_9 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[
        img_space1,
        img_space2,
        part_9_0])

    return [part_0, part_1, part_2, part_3, part_4, part_5, part_6, part_7, part_8, part_9], instructions
