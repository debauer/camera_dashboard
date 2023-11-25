from __future__ import annotations

from collections.abc import Callable
from contextlib import suppress
from multiprocessing import Event, Process
from multiprocessing.synchronize import Event as EventType
from typing import Any

from dashboard.interfaces.node import Node


class Isolator(Node):
    """Designed to isolate things into different processes instead of different
    threads to utilize multiple cores to the fullest extent.

    Some features will not be available if you use this one, most important of
    which is the registry.

    ATTENTION:
    We do not wait for the process to finish on shutdown. All processes are
    daemons that will be ignored when their parent dies. If you need a graceful
    shutdown then use the mechanisms provided by ShutdownAble and Main or use
    the MQTT-Topics concerning shutdown directly.
    """

    _MAX_WAIT_TIME = 30

    def __init__(
        self,
        target: Callable[..., Any],
        name: str | None = None,
        daemon: bool = True,
    ) -> None:
        Node.__init__(self)

        # explicitly set EventType as multiprocessing.Event is technically
        # a function not a type
        self._processing_shutdown_event: EventType = Event()
        self._name = name

        self._process = Process(
            target=self._work,
            args=(self._processing_shutdown_event, target),
            name=self._name,
            daemon=daemon,
        )

        self._process.start()

    def _work(
        self,
        processing_shutdown_event: EventType,
        action: Callable[..., Any],
    ) -> None:
        action()

        self.log.i(f"Created, now holding {self._name} alive", "_work")
        with suppress(KeyboardInterrupt):
            processing_shutdown_event.wait()

    def shutdown(self) -> None:
        self._processing_shutdown_event.set()
        if self._process.is_alive():
            self._process.join(Isolator._MAX_WAIT_TIME)
            self._process.kill()

        self.log.i(
            f"Isolator shutdown, name: {self._name}, still_alive: {self._process.is_alive()}",
            "_process",
        )
