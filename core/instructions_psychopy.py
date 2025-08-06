try:
    from psychopy.visual import ImageStim
except ModuleNotFoundError:
    try:
        from rewardgym.psychopy_render.psychopy_stubs import ImageStim
    except ModuleNotFoundError:
        from ....psychopy_render.psychopy_stubs import ImageStim
try:
    from ....stimuli import fixation_cross
except ImportError:
    from rewardgym.stimuli import fixation_cross

import json
import pathlib

instructions_path = (
    pathlib.Path(__file__).parent.resolve() / "assets" / "instructions_en.json"
)
instructions = json.loads(instructions_path.read_text())


def instructions_psychopy(instructions=instructions):
    fix = fixation_cross()

    def part_0(win, instructions):
        part_0_0 = ImageStim(win=win, image=fix, pos=(0, 0), size=fix.shape[:2])

        part_0_0.draw()

    return [part_0], instructions
