from __future__ import annotations

import itertools
from datetime import datetime
from typing import Literal, Tuple

import numpy
from numpy import frombuffer, reshape
from numpy.typing import NDArray

from .types import Box, Image

_ByteIntervall = Tuple[int, int]


def _int_to_bytes(
    number: int, length: int = 8, byteorder: Literal["little", "big"] = "little"
) -> bytes:
    return number.to_bytes(length=length, byteorder=byteorder)


def _bytes_to_int(
    byte_number: memoryview, byteorder: Literal["little", "big"] = "little"
) -> int:
    return int.from_bytes(byte_number, byteorder=byteorder)


def _get_int_from_bytes_interval(byte_msg: memoryview, interval: _ByteIntervall) -> int:
    return _bytes_to_int(byte_msg[interval[0] : interval[1]])


def _get_str_from_bytes_interval(byte_msg: memoryview, interval: _ByteIntervall) -> str:
    return bytes(byte_msg[interval[0] : interval[1]]).decode()


class EnrichedFrame:
    _MICRO_SECONDS = 10e6
    _id_iter = itertools.count()

    _HEIGHT_INTERVAL: _ByteIntervall = (0, 8)
    _WIDTH_INTERVAL: _ByteIntervall = (8, 16)
    _COLOR_INTERVAL: _ByteIntervall = (16, 24)
    _ID_INTERVAL: _ByteIntervall = (24, 32)
    _NAME_INTERVAL: _ByteIntervall = (32, 52)
    _TIMESTAMP_INTERVAL: _ByteIntervall = (52, 60)
    FRAME_OFFSET: int = _TIMESTAMP_INTERVAL[1]

    def __init__(
        self, camera_name: str, timestamp: datetime, frame: Image, frame_id: int = -1
    ) -> None:
        self.id = frame_id if frame_id > 0 else next(EnrichedFrame._id_iter)

        self.camera_name = camera_name
        self.timestamp = timestamp
        self.mapped_frame: Image | None = None
        self.frame = frame
        self.height, self.width = self.frame.shape[:2]

    def __str__(self) -> str:
        return f"EnrichedFrame: {{ id: {self.id}, camera_name: {self.camera_name}, }}"

    def to_bytes(self) -> bytes:
        height, width, color = self.frame.shape

        byte_height = _int_to_bytes(height)
        byte_width = _int_to_bytes(width)
        byte_color = _int_to_bytes(color)

        camera_name_size = (
            EnrichedFrame._NAME_INTERVAL[1] - EnrichedFrame._NAME_INTERVAL[0]
        )
        byte_name = self.camera_name.ljust(camera_name_size)[:camera_name_size].encode()
        byte_id = _int_to_bytes(self.id)
        byte_timestamp = _int_to_bytes(
            int(self.timestamp.timestamp() * self._MICRO_SECONDS)
        )
        byte_frame = self.frame.tobytes()

        result: bytes = (
            byte_height
            + byte_width
            + byte_color
            + byte_id
            + byte_name
            + byte_timestamp
            + byte_frame
        )
        return result

    @staticmethod
    def from_bytes(enriched_bytes: memoryview) -> EnrichedFrame:
        height = _get_int_from_bytes_interval(
            enriched_bytes, EnrichedFrame._HEIGHT_INTERVAL
        )
        width = _get_int_from_bytes_interval(
            enriched_bytes, EnrichedFrame._WIDTH_INTERVAL
        )
        color = _get_int_from_bytes_interval(
            enriched_bytes, EnrichedFrame._COLOR_INTERVAL
        )
        frame_id = _get_int_from_bytes_interval(
            enriched_bytes, EnrichedFrame._ID_INTERVAL
        )
        camera_name = _get_str_from_bytes_interval(
            enriched_bytes, EnrichedFrame._NAME_INTERVAL
        ).strip()
        timestamp = datetime.fromtimestamp(
            _get_int_from_bytes_interval(
                enriched_bytes, EnrichedFrame._TIMESTAMP_INTERVAL
            )
            / EnrichedFrame._MICRO_SECONDS
        )
        buffered_frame: NDArray[numpy.unit8] = frombuffer(  # type: ignore[name-defined]
            enriched_bytes, offset=EnrichedFrame.FRAME_OFFSET, dtype=numpy.uint8
        )
        frame = reshape(buffered_frame, (height, width, color))

        return EnrichedFrame(camera_name, timestamp, frame, frame_id=frame_id)
