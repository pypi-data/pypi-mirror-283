from __future__ import annotations

import argparse
from unittest import mock

import pytest


@pytest.fixture(autouse=True)
def _mock_argparse():
    with mock.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            port=8000,
            hostname="localhost",
        ),
    ):
        yield


@pytest.fixture(autouse=True)
def _mock_mixer():
    with mock.patch("pygame.mixer"):
        yield
