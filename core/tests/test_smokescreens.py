# Module name needs to be changed here:
try:
    from task_template.core import (
        get_configs,
        get_psychopy_info,
        get_pygame_info,
        get_task,
        instructions_psychopy,
    )
except (ModuleNotFoundError, ImportError):
    try:
        from . import (
            get_configs,
            get_psychopy_info,
            get_pygame_info,
            get_task,
            instructions_psychopy,
        )

    except (ModuleNotFoundError, ImportError):
        from rewardgym.tasks.task_template.core import (
            get_configs,
            get_pygame_info,
            get_psychopy_info,
            get_task,
            instructions_psychopy,
        )

import warnings


def test_get_configs():
    if get_configs is not None:
        out = get_configs("1")
        assert isinstance(out, dict)
    else:
        warnings.warn("Import of get_configs was None, is this intended?")


def test_get_pygame_info():
    if get_pygame_info is not None:
        out = get_pygame_info({0: "left", 1: "right"}, 120)
        assert isinstance(out, dict)
    else:
        warnings.warn("Import of test_get_pygame_info was None, is this intended?")


def test_get_psychopy_info():
    if get_psychopy_info is not None:
        a, b = get_psychopy_info()
        assert isinstance(a, dict)
        assert isinstance(b, dict) or (b is None)
    else:
        warnings.warn("Import of test_get_psychopy_info was None, is this intended?")


def test_get_task():
    a, b, c = get_task()

    assert isinstance(a, dict)
    assert isinstance(b, dict)
    assert isinstance(c, dict)


def test_instructions_psychopy():
    if instructions_psychopy is not None:
        a, b = instructions_psychopy()

        assert isinstance(a, list)
        assert isinstance(b, dict)

    else:
        warnings.warn("Import of instructions_psychopy was None, is this intended?")
