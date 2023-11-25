from __future__ import annotations

from http.server import HTTPServer
from socketserver import ThreadingMixIn
from threading import Event

from dashboard.datatypes import Image


class FrameServer(ThreadingMixIn, HTTPServer):
    frame: Image
    shutdown_event: Event
    num_classes: int = 1000
