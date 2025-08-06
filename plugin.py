"""
Plugin function to register tasks. It should not be necessary to change it.
"""

from .core import get_task

try:
    from .core import get_configs
except ImportError:
    get_configs = None

try:
    from .core import get_psychopy_info
except (ImportError, NameError):
    get_psychopy_info = None

try:
    from .core import get_pygame_info
except (ImportError, NameError):
    get_pygame_info = None

try:
    from .core import instructions_psychopy
except (ImportError, NameError):
    instructions_psychopy = None

import pathlib

import yaml


def register_task():
    yaml_file = pathlib.Path(__file__).parent.resolve() / "task.yaml"
    with open(yaml_file, "r") as f:
        raw = yaml.safe_load(f)

    return {
        raw["meta"]["name"]: {
            "get_task": get_task,
            "get_configs": get_configs,
            "get_pygame_info": get_pygame_info,
            "get_psychopy_info": get_psychopy_info,
            "instructions_psychopy": instructions_psychopy,
        }
    }
