from __future__ import annotations

import os
import time

import pytest

from garmi_gui import gui

# set SDL to use the dummy NULL video driver,
#   so it doesn't need a windowing system.
os.environ["SDL_VIDEODRIVER"] = "dummy"


def test_gui():
    gui_instance = gui.GUI(8000, fullscreen=False, testing=True)

    gui_instance.show_image("eyes.png")
    time.sleep(0.1)
    gui_instance.play_sound("confirm.wav")
    time.sleep(0.1)
    gui_instance.stop_sound()
    gui_instance.show_video("simulation.mp4")
    time.sleep(1)
    gui_instance.show_text("Test", color=(255, 255, 255), font_size=10)
    time.sleep(0.1)
    gui_instance.render_text(
        "line1\nline2\nline3", speed=15, color=(255, 0, 0), font_size=50
    )
    time.sleep(1)

    assert gui_instance.process_path("relative/path") != "relative/path"
    assert "resources" in gui_instance.process_path("relative/path")

    with pytest.raises(FileNotFoundError):
        gui_instance.show_image("unknown-image-path")
    with pytest.raises(FileNotFoundError):
        gui_instance.show_video("unknown-video-path")

    assert (
        len(
            gui_instance.wrap_text(
                "This text should be wrapped.", font_size=200
            ).splitlines()
        )
        > 1
    )

    assert gui_instance.screen.get_rect().width == 1280
    assert gui_instance.screen.get_rect().height == 960

    gui_instance.stop()
