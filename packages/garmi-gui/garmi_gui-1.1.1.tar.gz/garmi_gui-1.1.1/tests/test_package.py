from __future__ import annotations

import importlib.metadata

import garmi_gui as m


def test_version():
    assert importlib.metadata.version("garmi_gui") == m.__version__
