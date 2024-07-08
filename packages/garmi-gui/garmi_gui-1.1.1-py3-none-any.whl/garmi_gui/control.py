# ruff: noqa: T201
from __future__ import annotations

import argparse
import xmlrpc.client

import simple_term_menu  # type: ignore[import-not-found]


def main() -> None:
    """Simple terminal program that allows you to connect to a GARMI GUI remotely
    and execute commands. If you installed the package this function is installed
    as an executable that can be called as
    ``garmi-gui --hostname <gui-hostname> --port <gui-port>`` to connect with a
    remote GUI running on the given hostname and port respectively.
    """
    parser = argparse.ArgumentParser(description="Remote GUI Controller")
    parser.add_argument(
        "--hostname", type=str, default="localhost", help="Hostname of the remote GUI"
    )
    parser.add_argument("--port", type=int, default=8000, help="Port of the remote GUI")
    args = parser.parse_args()

    server_url = f"http://{args.hostname}:{args.port}"
    proxy = xmlrpc.client.ServerProxy(server_url)

    menu = simple_term_menu.TerminalMenu(
        ["Show Image", "Play Sound", "Show Video", "Show Text", "Render Text", "Exit"]
    )
    while True:
        choice = menu.show()

        if choice == 0:
            image_path = input("Enter the path to the image: ")
            proxy.show_image(image_path)
            print(f"Image '{image_path}' displayed.")
        elif choice == 1:
            sound_path = input("Enter the path to the sound file: ")
            proxy.play_sound(sound_path)
            print(f"Sound '{sound_path}' played.")
        elif choice == 2:
            video_path = input("Enter the path to the video file: ")
            proxy.show_video(video_path)
            print(f"Video '{video_path}' displayed.")
        elif choice == 3:
            print("Enter the text to display: ")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            text = "\n".join(lines)
            color_str = input("Enter the color (default is 0,255,255 cyan): ")
            font_size_str = input("Enter the font size (default is 100): ")
            color = (
                tuple(map(int, color_str.split(","))) if color_str else (0, 255, 255)
            )
            font_size = int(font_size_str) if font_size_str else 100
            proxy.show_text(text, color, font_size)
            print(f"Text '{text}' displayed.")
        elif choice == 4:
            print("Enter the text to render (finish input by entering an empty line):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            text = "\n".join(lines)
            speed_str = input(
                "Enter the speed (characters per second, default is 10): "
            )
            color_str = input("Enter the color (default is 0,255,255 cyan): ")
            font_size_str = input("Enter the font size (default is 100): ")
            speed = int(speed_str) if speed_str else 10
            color = (
                tuple(map(int, color_str.split(","))) if color_str else (0, 255, 255)
            )
            font_size = int(font_size_str) if font_size_str else 100
            proxy.render_text(text, speed, color, font_size)
            print(f"Text '{text}' rendered.")
        elif choice == 5:
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
