from __future__ import annotations

from unittest import mock

from garmi_gui import control


@mock.patch("builtins.input", return_value="6")
def test_control(*args):
    del args
    control.main()
