from __future__ import annotations

import argparse
import pathlib
import textwrap
import threading
from xmlrpc import server

import cv2
import pygame

RESOURCE_PATH = pathlib.Path(pathlib.Path(__file__).parent) / "resources"


class GUI:
    """GUI for the GARMI robot face display.

    The functions of this class are usually called remotely using xmlrpc."""

    def __init__(self, port: int, fullscreen: bool = True, testing: bool = False):
        self.fullscreen = fullscreen
        self.testing = testing
        self.screen_initialized = threading.Event()
        self.video_thread: None | threading.Thread = None
        self.video_running = False
        self.sound: None | pygame.mixer.Sound = None
        self.stop_video_event = threading.Event()
        self.running = True
        self.mux = threading.Lock()

        self.gui_thread = threading.Thread(target=self._run)
        self.gui_thread.start()
        self.screen_initialized.wait()
        self.show_image("eyes.png")

        self.server = server.SimpleXMLRPCServer(("0.0.0.0", port), allow_none=True)
        self.server.register_instance(self)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()

    def play_sound(self, sound_path: str) -> None:
        """Plays a local sound file. If only a filename is given,
        the file is searched for in the local resources directory."""
        self.stop_sound()
        self.sound = pygame.mixer.Sound(self.process_path(sound_path))
        self.sound.play()

    def process_path(self, path: str) -> str:
        proc_path = pathlib.Path(path).expanduser()
        if proc_path.is_absolute():
            return str(proc_path)
        return str(RESOURCE_PATH / proc_path)

    def stop_sound(self) -> None:
        """Stops playing sound if the GUI is currently playing a sound."""
        if self.sound is not None:
            self.sound.stop()

    def wrap_text(self, text: str, font_size: int) -> str:
        """Wraps a textstring so it will fit into the screen when displayed.
        :py:func:`render_text` and :py:func:`show_text` will apply this to
        any text arguments before rendering."""
        proc: list[str] = []
        for line in text.splitlines():
            wrapped = textwrap.wrap(
                line,
                int(100 / font_size * 35 * self.screen.get_rect().width / 1280),
                drop_whitespace=False,
                replace_whitespace=False,
            )
            if wrapped:
                proc.extend(wrapped)
            else:
                proc.append("")
        return str.join("\n", proc)

    def show_text(
        self,
        text: str,
        color: tuple[int, int, int] = (0, 255, 255),
        font_size: int = 100,
    ) -> None:
        """Displays a text on the GUI in the given color and font size.
        The displayed text may contain newline but is also wrapped to fit the display."""
        text = self.wrap_text(text, font_size)
        self.stop_video()
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, font_size)
        lines = text.splitlines()
        bias_y = (len(lines) - 1) / 2 * font_size
        with self.mux:
            for line_number, line in enumerate(lines):
                text_surface = font.render(line, True, color)
                pos = list(self.screen.get_rect().center)
                pos[1] += int(font_size * line_number - bias_y)
                text_rect = text_surface.get_rect(center=pos)
                self.screen.blit(text_surface, text_rect)

    def render_text(
        self,
        text: str,
        speed: int = 10,
        color: tuple[int, int, int] = (0, 255, 255),
        font_size: int = 100,
    ) -> None:
        """Renders text on the GUI character by character with the speed
        given in characters per second. Wraps text as necessary. Otherwise
        functions like :py:func:`show_text`."""
        self.stop_video()
        text = self.wrap_text(text, font_size)

        def render() -> None:
            font = pygame.font.Font(None, font_size)
            rendered_lines: list[tuple[pygame.Surface, pygame.Rect]] = []
            lines = text.splitlines()
            bias_y = (len(lines) - 1) / 2 * font_size
            for line_number, line in enumerate(lines):
                current_text = ""
                for char in line:
                    if not self.running:
                        break
                    current_text += char
                    text_surface = font.render(current_text, True, color)
                    pos = list(self.screen.get_rect().center)
                    pos[1] += int(font_size * line_number - bias_y)
                    text_rect = text_surface.get_rect(center=pos)
                    with self.mux:
                        self.screen.fill((0, 0, 0))
                        for surface, rect in rendered_lines:
                            self.screen.blit(surface, rect)
                        self.screen.blit(text_surface, text_rect)
                    self.clock.tick(speed)
                rendered_lines.append((text_surface, text_rect))

        threading.Thread(target=render).start()

    def show_image(self, image_path: str) -> None:
        """Displays a local image on the GUI. Relative paths are evaluated
        relative to the resources directory."""
        self.stop_video()
        image = pygame.image.load(self.process_path(image_path)).convert()
        image = pygame.transform.smoothscale(image, self.screen.get_size())
        with self.mux:
            self.screen.blit(image, (0, 0))

    def show_video(self, video_path: str) -> None:
        """Plays a local video and displays it on the GUI.
        The video will loop until something else is displayed
        or :py:func:`stop_video` is called."""
        video_path = self.process_path(video_path)
        self.stop_video()
        if not pathlib.Path(video_path).exists():
            raise FileNotFoundError()
        self.video_thread = threading.Thread(
            target=self._play_video, args=(video_path,)
        )
        self.video_thread.start()

    def _play_video(self, video_path: str) -> None:
        self.video_running = True
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)

        while self.video_running and self.running:
            if self.stop_video_event.is_set():
                break
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB")
            with self.mux:
                self.screen.blit(
                    pygame.transform.smoothscale(frame, self.screen.get_size()), (0, 0)
                )

            self.clock.tick(fps)

        cap.release()
        self.video_running = False

    def stop_video(self) -> None:
        """Stops video if a video is currently shown on the GUI."""
        if self.video_running and self.video_thread is not None:
            self.stop_video_event.set()
            self.video_thread.join()
            self.stop_video_event.clear()

    # pylint: disable=attribute-defined-outside-init
    def _run(self) -> None:
        pygame.init()
        if not self.fullscreen:
            self.screen = pygame.display.set_mode((1280, 960))
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("garmi-head GUI")
        self.clock = pygame.time.Clock()
        pygame.display.flip()
        self.screen_initialized.set()

        if self.testing:
            return

        while self.running:
            try:
                for event in pygame.event.get():
                    if (
                        event.type == pygame.QUIT
                        or event.type == pygame.KEYDOWN
                        and event.key == pygame.K_ESCAPE
                    ):
                        self.running = False
                with self.mux:
                    pygame.display.flip()
            except pygame.error:
                self.running = False

            self.clock.tick(30)  # Throttle loop to reduce CPU usage

        self.stop()

    def stop(self) -> None:
        """Closes the GUI and stops any connected threads."""
        self.stop_video()
        self.server.shutdown()
        self.server_thread.join()
        pygame.quit()


def start_gui() -> None:
    """This function is installed as an executable and can be run as
    ``garmi-gui --port <port>`` where an xmlrpc server is started, listening
    on the given port."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port", "-p", type=int, default=8000, help="Port of the xmlrpc server."
    )
    parser.add_argument(
        "--windowed",
        action="store_true",
        help="Set to run in windowed mode (default is fullscreen)",
    )
    args = parser.parse_args()
    app = GUI(args.port, fullscreen=not args.windowed)
    try:
        app.gui_thread.join()
    except KeyboardInterrupt:
        app.stop()


if __name__ == "__main__":
    start_gui()
