from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from time import time
from urllib.parse import parse_qs, urlparse

from cv2 import INTER_NEAREST, imencode, resize

from dashboard.datatypes import Dimensions, Image
from dashboard.stream.frame_server import FrameServer


class MjpegHandler(BaseHTTPRequestHandler):
    server: FrameServer
    __default_resolution: str = "320x240"
    __default_neural: str = "false"
    __default_fps: int = 3

    @staticmethod
    def __get_resolution(resolution: list[str] | str) -> Dimensions:
        splitted = (resolution if isinstance(resolution, str) else resolution[0]).split(
            "x"
        )
        return Dimensions(int(splitted[0]), int(splitted[1]))

    def do_GET(self) -> None:
        result = urlparse(self.path)
        parameter: dict[str, list[str]] = parse_qs(result.query)
        self.send_response(200)
        self.send_header(
            "Content-type", "multipart/x-mixed-replace; boundary=--jpgboundary"
        )
        self.end_headers()
        resolution = parameter.get("resolution", self.__default_resolution)
        neural_active = parameter.get("neural", self.__default_neural)
        fps_arg = parameter.get("fps", self.__default_fps)
        fps = self.__default_fps if not isinstance(fps_arg, str) else int(fps_arg)  # type: ignore[arg-type, unreachable]

        width, height = self.__get_resolution(resolution)

        try:
            from mlcvzoo_base.utils import draw_on_image  # type: ignore[attr-defined] # noqa: I001
            from mlcvzoo_base.utils import generate_detector_colors  # type: ignore[attr-defined]

            rgb_colors: list[tuple[int, int, int]] | None = generate_detector_colors(
                num_classes=self.server.num_classes,
            )
        except ModuleNotFoundError:
            rgb_colors = None
            draw_on_image = None  # type: ignore[assignment]

        time_between_frames = 1 / fps
        start_time = time()
        frame_count = 0
        while not self.server.shutdown_event.is_set():
            try:
                if (
                    draw_on_image is not None
                    and rgb_colors is not None
                    and self.server.boxes is not None
                    and neural_active != self.__default_neural
                ):
                    # bounding boxes are structurally identical to SandBoxes
                    try:
                        draw_frame = draw_on_image(
                            frame=self.server.frame,
                            rgb_colors=rgb_colors,
                            bounding_boxes=self.server.boxes.boxes,  # type: ignore[arg-type]
                        )
                    except AttributeError:
                        draw_frame = self.server.frame
                else:
                    draw_frame = self.server.frame
                resized: Image = resize(
                    draw_frame, (width, height), interpolation=INTER_NEAREST
                )
                _ret, jpeg = imencode(".jpeg", resized)
                self.wfile.write(b"--jpgboundary\r\n")
                self.send_header("Content-type", "image/jpeg")
                self.send_header("Content-length", str(jpeg.size))
                self.end_headers()
                self.wfile.write(jpeg.tostring())
                frame_count += 1
                next_frame_time = start_time + frame_count * time_between_frames
                while (
                    not self.server.shutdown_event.is_set() and time() < next_frame_time
                ):
                    # wait on shutdown_event to recognize shutdown
                    self.server.shutdown_event.wait(time_between_frames)
            except BrokenPipeError:
                break
