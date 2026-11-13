# Module name needs to be changed here:
try:
    from twostep.core import (
        get_configs,
        get_render_info,
        get_task,
        instructions_psychopy,
    )
except (ModuleNotFoundError, ImportError):
    try:
        from . import (
            get_configs,
            get_render_info,
            get_task,
            instructions_psychopy,
        )

    except (ModuleNotFoundError, ImportError):
        from rewardgym.tasks.twostep.core import (
            get_configs,
            get_render_info,
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


def test_get_render_info():
    if get_render_info is not None:
        a, b = get_render_info()
        assert isinstance(a, dict)
        assert isinstance(b, dict) or (b is None)
    else:
        warnings.warn("Import of test_get_render_info was None, is this intended?")


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
