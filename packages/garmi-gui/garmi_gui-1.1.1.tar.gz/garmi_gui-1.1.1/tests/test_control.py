from __future__ import annotations

from unittest import mock

from garmi_gui import control


@mock.patch("simple_term_menu.TerminalMenu")
def test_exit(mock_show):
    mock_show.return_value.show.return_value = 5
    control.main()


@mock.patch("builtins.input", return_value="test.png")
@mock.patch("simple_term_menu.TerminalMenu")
@mock.patch("xmlrpc.client.ServerProxy")
def test_show_image(mock_proxy, mock_show, mock_input):
    del mock_input
    mock_show.return_value.show.side_effect = [0, 5]
    control.main()
    mock_proxy.return_value.show_image.assert_called_once_with("test.png")


@mock.patch("builtins.input", return_value="test.wav")
@mock.patch("simple_term_menu.TerminalMenu")
@mock.patch("xmlrpc.client.ServerProxy")
def test_play_sound(mock_proxy, mock_show, mock_input):
    del mock_input
    mock_show.return_value.show.side_effect = [1, 5]
    control.main()
    mock_proxy.return_value.play_sound.assert_called_once_with("test.wav")


@mock.patch("builtins.input", return_value="test.mp4")
@mock.patch("simple_term_menu.TerminalMenu")
@mock.patch("xmlrpc.client.ServerProxy")
def test_show_video(mock_proxy, mock_show, mock_input):
    del mock_input
    mock_show.return_value.show.side_effect = [2, 5]
    control.main()
    mock_proxy.return_value.show_video.assert_called_once_with("test.mp4")


@mock.patch("builtins.input", side_effect=["line1", "line2", "", "255, 255, 255", "75"])
@mock.patch("simple_term_menu.TerminalMenu")
@mock.patch("xmlrpc.client.ServerProxy")
def test_show_text(mock_proxy, mock_show, mock_input):
    del mock_input
    mock_show.return_value.show.side_effect = [3, 5]
    control.main()
    mock_proxy.return_value.show_text.assert_called_once_with(
        "line1\nline2", (255, 255, 255), 75
    )


@mock.patch(
    "builtins.input", side_effect=["line1", "line2", "", "15", "255, 255, 255", "75"]
)
@mock.patch("simple_term_menu.TerminalMenu")
@mock.patch("xmlrpc.client.ServerProxy")
def test_render_text(mock_proxy, mock_show, mock_input):
    del mock_input
    mock_show.return_value.show.side_effect = [4, 5]
    control.main()
    mock_proxy.return_value.render_text.assert_called_once_with(
        "line1\nline2", 15, (255, 255, 255), 75
    )
