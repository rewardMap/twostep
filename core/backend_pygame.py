try:
    from ....pygame_render import BaseAction, BaseDisplay, BaseText, feedback_block
except ImportError:
    from rewardgym.pygame_render import (
        BaseAction,
        BaseDisplay,
        BaseText,
        feedback_block,
    )


def get_pygame_info(action_map, window_size=256):
    base_position = (window_size // 2, window_size // 2)

    reward_disp, earnings_text = feedback_block(base_position)

    final_display = [
        BaseDisplay(None, 1),
        reward_disp,
        earnings_text,
    ]

    def first_step(text):
        return [
            BaseDisplay(None, 1),
            BaseText("+", 500, textposition=base_position),
            BaseDisplay(None, 1),
            BaseText(text, 50, textposition=base_position),
            BaseAction(),
        ]

    pygame_dict = {
        0: {"pygame": first_step("A       or       B")},
        1: {"pygame": first_step("C       or       D")},
        2: {"pygame": first_step("E       or       F")},
        3: {"pygame": final_display},
        4: {"pygame": final_display},
        5: {"pygame": final_display},
        6: {"pygame": final_display},
    }

    return pygame_dict
