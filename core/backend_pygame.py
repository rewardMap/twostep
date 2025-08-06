try:
    from ....pygame_render import BaseText
except ImportError:
    from rewardgym.pygame_render import BaseText


def get_pygame_info(action_map, window_size=256):
    base_position = (window_size // 2, window_size // 2)

    final_display = BaseText("+", 500, textposition=base_position)
    pygame_dict = {
        0: {"pygame": [final_display]},
    }

    return pygame_dict
