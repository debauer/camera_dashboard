#!/usr/bin/env python
from argparse import ArgumentParser
from logging import getLogger, DEBUG
from multiprocessing import Event
from time import sleep
from typing import Any

from dashboard.config import DeviceConfig
from dashboard.interfaces.node import Node
from dashboard.reader.rtsp import RtspReader

_shutdown_event = Event()
_nodes: list[Node] = []


def get_args() -> Any:
    parser = ArgumentParser(description="yolo")
    parser.add_argument(
        "--log",
        type=str,
        default="DEBUG",
        help="Set the loglevel for the stdout-Logging, see '--general-log' for other options; "
        "values are: WARNING, INFO, DEBUG",
    )
    return parser.parse_args()


def run() -> None:
    args = get_args()
    loglevel = args.log
    _nodes = [
        RtspReader(
            DeviceConfig(
                name="C200_1",
                serve_port=8001,
                stream="rtsp://192.168.1.16/axis-media/media.amp?resolution=2560x1440",
                stream_resolution="2560x1440"
            ),
            device_name="C200_1"
        ),
        RtspReader(
            DeviceConfig(
                name="C200_2",
                serve_port=8002,
                stream="rtsp://192.168.1.16/axis-media/media.amp?resolution=2560x1440",
                stream_resolution="2560x1440"
            ),
            device_name="C200_2"
        )
    ]
    for n in _nodes:
        n.start()
    while not _shutdown_event.is_set():
        try:
            sleep(0.1)
        except KeyboardInterrupt:
            _shutdown_event.set()
            for n in _nodes:
                n.shutdown()


if __name__ == "__main__":
    run()
