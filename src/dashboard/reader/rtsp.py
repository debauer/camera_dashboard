from asyncio import Event
from typing import Any

from cv2 import (
    error as CVError,
    VideoCapture,
    CAP_PROP_BUFFERSIZE,
    CAP_PROP_FOURCC,
    resize, imread, INTER_AREA,
    VideoWriter_fourcc
)

from dashboard.config import DeviceConfig
from dashboard.datatypes import Image, Dimensions
from dashboard.interfaces.util import NamedCollectAble, EnrichedSubscriber
from dashboard.util.time import now
from dashboard.datatypes.frame import EnrichedFrame
from dashboard.interfaces.node import Node


class _CannotOpenStreamException(Exception):
    pass


class _ImageCapture(VideoCapture):  # type: ignore[misc]
    """Convenience class so the image replay doesn't give as many errors."""

    _image: Image

    def __init__(
            self,
            path: str,
            resize_dimension: Dimensions,
            *args: Any,
            **kwargs: Any,
    ) -> None:
        self._image = resize(imread(path), resize_dimension, interpolation=INTER_AREA)
        super().__init__(*args, **kwargs)

    def isOpened(self) -> bool:
        return True

    def set(self, *_: Any) -> None:  # noqa: A003
        pass

    def release(self) -> None:
        pass

    def getExceptionMode(self) -> str:
        return "static jpeg mode"

    def grab(self) -> bool:
        return True

    def retrieve(
            self, image: Any = None, flag: Any = None  # noqa: ARG002
    ) -> tuple[bool, Image]:
        return True, self._image


class RtspReader(Node, NamedCollectAble[EnrichedSubscriber]):

    def __init__(
            self,
            device_config: DeviceConfig,
            device_name: str,
    ) -> None:
        Node.__init__(self)
        self.config = device_config
        self._name = device_name
        self._fps = self.config.fps
        # log intermediary statistic every {self.fps}-frames in the first minute
        self._verbose_log_frame_count = self._fps * 60

        # after that log them once every 10 minutes
        self._non_verbose_log_frame_count = self._fps * 60 * 10

        self._stream_updated = Event()

        self.create_thread(
            target=self._open_camera,
            args=(),
            name=f"r_{self._name}",
            start=False,
        )

    def _open_camera(self) -> None:
        fct = "open_cam"
        try:
            while not self.shutdown_event.is_set():
                try:
                    stream = self._get_capture()
                except _CannotOpenStreamException:
                    self.shutdown_event.wait(1)
                    continue

                (
                    successful_grab,
                    successful_retrieve,
                ) = self._record_stream(stream)

                stream.release()
        except CVError:
            self.log.exception("Critical error while reading from camera", fct)

        self.log.w(f"Shutting down CameraReader for {self._name}", fct)

    def get_name(self) -> str:
        return self._name

    def start(self) -> None:
        """This method start all threads that were prepared in `__init__`."""
        self.start_all_threads()

    def _record_stream(self, stream: VideoCapture) -> tuple[bool, bool]:
        successful_retrieve = True
        successful_grab = True

        while (
                successful_grab and successful_retrieve and not self.shutdown_event.is_set()
        ):
            successful_grab = stream.grab()
            successful_retrieve, frame = stream.retrieve()
            self._publish(
                frame,
                successful_grab,
                successful_retrieve,
            )

            if self._stream_updated.is_set():
                self._stream_updated.clear()
                return True, True

        return successful_grab, successful_retrieve

    def _get_stream(self) -> str | int:
        stream = self.config.stream

        try:
            return int(stream)
        except ValueError:
            return stream

    def _get_capture(self) -> VideoCapture:
        fct = "_get_capture"
        stream = self._get_stream()

        if str(stream).endswith(".jpg"):
            self.log.d(f"Opening stream with ImageCapture: {stream}", fct)
            capture = _ImageCapture(
                str(stream), resize_dimension=self.config.stream_resolution
            )
        else:
            self.log.d(f"Opening stream with VideoCapture: {stream}", fct)
            capture = VideoCapture(stream)

        if not capture.isOpened():
            self.log.w(f"Error when opening stream: {stream}", fct)
            raise _CannotOpenStreamException

        stream_buffer_size = 1
        capture.set(CAP_PROP_BUFFERSIZE, stream_buffer_size)
        capture.set(CAP_PROP_FOURCC, VideoWriter_fourcc("M", "J", "P", "G"))

        return capture

    def _publish(
            self,
            frame: Image,
            successful_grab: bool,
            successful_retrieve: bool,
    ) -> None:
        if not successful_grab or not successful_retrieve:
            return

        enriched_frame = EnrichedFrame(self._name, now(), frame)
        for subscriber in self.subscribers:
            subscriber.push_frame(enriched_frame)
