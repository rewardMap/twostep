try:
    from psychopy.visual import ImageStim, TextBox2, Line, TextStim
except ModuleNotFoundError:
    try:
        from rewardgym.psychopy_render.psychopy_stubs import ImageStim, TextBox2, Line, TextStim
    except ModuleNotFoundError:
        from ....psychopy_render.psychopy_stubs import ImageStim, TextBox2, Line, TextStim
try:
    from ....stimuli import zero_cross, win_cross, lose_cross
except ImportError:
    from rewardgym.stimuli import zero_cross, win_cross, lose_cross

from .backend_psychopy import two_step_alien_images
import json
import numpy as np
import pathlib

# Instructions modeled after
# Feher da Silva, C., Lombardi, G., Edelson, M., & Hare, T. A. (2023). Rethinking model-based and model-free influences on mental effort and striatal prediction errors. Nature Human Behaviour, 7(6), 956–969. https://doi.org/10.1038/s41562-023-01573-1
# Adjusted to space travel and trading.

instructions_path = (
    pathlib.Path(__file__).parent.resolve() / "assets" / "instructions_new.json"
)
instructions = json.loads(instructions_path.read_text())


def instructions_psychopy(instructions=instructions):

    stimulus_colors = {
        "colors": [
             (0, 0, 200),
             (200, 200, 0),
             (0, 150, 200),
             (0, 150, 200),
        ]
    }

    stimuli, _ = two_step_alien_images(random_state=1, stim_defaults=stimulus_colors)

    def part_0(win, instructions):
        part_0_0 = TextBox2(
            win=win,
            text=instructions["0.0"],
            letterHeight=28,
            pos=(0, 200),
        )

        part_0_0.draw()

    def part_1(win, instructions):
        part_1_0 = TextBox2(
            win=win,
            text=instructions["1.0"],
            letterHeight=28,
            pos=(0, 200),
        )

        part_1_1 = TextBox2(
            win=win,
            text=instructions["1.1"],
            letterHeight=28,
            pos=(0, -100),
        )

        size = (100, 100)
        # img_space = ImageStim(win=win, image=stimuli[0][0], pos=(0, 20), size=size)
        img_planet1 = ImageStim(win=win, image=stimuli[1][2], pos=(-200, 20), size=size)
        img_planet2 = ImageStim(win=win, image=stimuli[2][2], pos=(200, 20), size=size)

        img_alien1 = ImageStim(win=win, image=stimuli[1][0], pos=(-320, -190), size=size)
        img_alien2 = ImageStim(win=win, image=stimuli[1][1], pos=(-120, -190), size=size)

        img_alien3 = ImageStim(win=win, image=stimuli[2][0], pos=(120, -190), size=size)
        img_alien4 = ImageStim(win=win, image=stimuli[2][1], pos=(320, -190), size=size)

        for i in [
           #  img_space,
            img_planet1,
            img_planet2,
            img_alien1,
            img_alien2,
            img_alien3,
            img_alien4,
            part_1_0,
            part_1_1,

        ]:
            i.draw()

    def part_2(win, instructions):
        size= (100, 100)

        nothing = zero_cross(
            width=100, height=100, circle_radius_inner=10, circle_radius_outer=15
        )
        winning = win_cross(
            width=100, height=100, circle_radius_inner=10, circle_radius_outer=15
        )

        part_1_0 = TextBox2(
            win=win,
            text=instructions["2.0"],
            letterHeight=28,
            pos=(0, 250),
        )
        part_1_1 = TextBox2(
            win=win,
            text=instructions["2.1"],
            letterHeight=28,
            pos=(0, 40),
        )

        img_alien1 = ImageStim(win=win, image=stimuli[1][0], pos=(-160, 150), size=size)

        img_alien2 = ImageStim(win=win, image=stimuli[1][0], pos=(-160, -100), size=size)

        img_win = ImageStim(win=win, image=winning, pos=(0, 150), size=winning.shape[:2])
        img_lose = ImageStim(win=win, image=nothing, pos=(0, -100), size=winning.shape[:2])

        for i in [
            part_1_0,
            part_1_1,
            img_alien1,
            img_alien2,
            img_win,
            img_lose,
        ]:
            i.draw()

    def part_3(win, instructions):
        part_3_0 = TextBox2(
            win=win,
            text="\n\n".join([instructions["3.0"],instructions["3.1"],instructions["3.2"]]),
            letterHeight=28,
            pos=(0, 250),
        )

        for i in [
            part_3_0]:
            i.draw()

    def part_4(win, instructions):
        part_4_0 = TextBox2(
            win=win,
            text="\n\n".join([instructions["4.0"],instructions["4.1"],instructions["4.2"]]),
            letterHeight=28,
            pos=(0, 250),
        )

        for i in [
            part_4_0]:
            i.draw()

    def part_5(win, instructions):
        part_5_0 = TextBox2(
            win=win,
            text=instructions["5.0"] + "\n\n" + instructions["5.1"],
            letterHeight=28,
            pos=(0, 250),
        )

        part_5_1 = TextBox2(
            win=win,
            text=instructions["5.2"],
            letterHeight=28,
            pos=(-350, 100),
            size=(400, None)
        )

        part_5_2 = TextBox2(
            win=win,
            text=instructions["5.3"],
            letterHeight=28,
            pos=(350, 100),
            size=(400, None)
        )

        size = (100, 100)
        img_space1 = ImageStim(win=win, image=stimuli[0][0], pos=(-350, -50), size=size)
        img_space2 = ImageStim(win=win, image=stimuli[0][1], pos=(350, -50), size=size)

        img_planet1 = ImageStim(win=win, image=stimuli[1][2], pos=(-350, -200), size=size)
        img_planet2 = ImageStim(win=win, image=stimuli[2][2], pos=(350, -200), size=size)

        for i in [
            img_space1,
            img_space2,
            img_planet1,
            img_planet2,
            part_5_0,
            part_5_1,
            part_5_2,
        ]:
            i.draw()

    def part_6(win, instructions):
        part_6_0 = TextBox2(
            win=win,
            text=instructions["6.0"] + "\n\n" + instructions["6.1"],
            letterHeight=28,
            pos=(0, 275),
        )

        part_6_2 = TextBox2(
            win=win,
            text=instructions["6.2"],
            letterHeight=28,
            pos=(0, -250),
        )

        size = (400, 400)
        img_space1 = ImageStim(win=win, image=stimuli[0][0], pos=(-325, 0), size=size)
        img_space2 = ImageStim(win=win, image=stimuli[0][1], pos=(325, 0), size=size)

        for i in [
            img_space1,
            img_space2,
            part_6_0,
            part_6_2,
        ]:
            i.draw()


    def part_7(win, instructions):
        part_7_0 = TextBox2(
            win=win,
            text=instructions["7.0"] + "\n\n" + instructions["7.1"] + "\n\n" + instructions["7.2"],
            letterHeight=28,
            pos=(0, 250),
            size=(1000, None)
        )
        part_7_3 = TextBox2(
            win=win,
            text=instructions["7.3"],
            letterHeight=28,
            pos=(0, -300),
            size=(1000, None)
        )

        size = (100, 100)
        img_space1 = ImageStim(win=win, image=stimuli[0][0], pos=(-200, 25), size=size)

        img_planet1 = ImageStim(win=win, image=stimuli[1][2], pos=(-200, -125), size=size)
        img_planet2 = ImageStim(win=win, image=stimuli[2][2], pos=(200, -125), size=size)

        arrow_text1 = TextStim(
            win=win,
            text='↓',  # Unicode down arrow
            color='white',
            height=100,
            pos=(-200, -65)
        )

        arrow_text2 = TextStim(
            win=win,
            text='↓',  # Unicode down arrow
            color='white',
            height=100,
            pos=(0, -65),
            ori=-45
        )

        x_text = TextStim(
            win=win,
            text='X',  # Unicode down arrow
            color='red',
            height=50,
            pos=(-200, -65)
        )

        for i in [
            img_space1,
            img_planet1,
            img_planet2,
            part_7_0,
            part_7_3,
            arrow_text1,
            arrow_text2,
            x_text,
        ]:
            i.draw()

    def part_8(win, instructions):
        part_8_0 = TextBox2(
            win=win,
            text=instructions["8.0"] + "\n\n" + instructions["8.1"],
            letterHeight=28,
            pos=(0, 250),
            size=(1000, None)
        )

        part_8_2 = TextBox2(
            win=win,
            text=instructions["8.2"],
            letterHeight=28,
            pos=(0, -250),
            size=(1000, None)
        )

        size = (400, 400)
        img_space1 = ImageStim(win=win, image=stimuli[1][0], pos=(-325, 0), size=size)
        img_space2 = ImageStim(win=win, image=stimuli[1][1], pos=(325, 0), size=size)

        for i in [
            img_space1,
            img_space2,
            part_8_0,
            part_8_2,
        ]:
            i.draw()


    def part_9(win, instructions):
        part_9_0 = TextBox2(
            win=win,
            text=instructions["9.0"] + "\n\n" + instructions["9.1"],
            letterHeight=28,
            pos=(0, 250),
            size=(1000, None)
        )

        size = (400, 400)
        img_space1 = ImageStim(win=win, image=stimuli[1][0], pos=(325, 0), size=size)
        img_space2 = ImageStim(win=win, image=stimuli[1][1], pos=(-325, 0), size=size)

        for i in [
            img_space1,
            img_space2,
            part_9_0,
        ]:
            i.draw()

    return [part_0, part_1, part_2, part_3, part_4, part_5, part_6, part_7, part_8, part_9], instructions
