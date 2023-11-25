from __future__ import annotations

from collections.abc import Callable
from threading import Thread, Event
from typing import Any, TypeVar

from dashboard.logger import Logger

T = TypeVar("T")
class Node:
    def __init__(self) -> None:

        self.log = Logger(self.__class__.__name__)
        self._threads: list[Thread] = []
        self.shutdown_event = Event()
        self.subscribers: list[T] = []

    def create_thread(
        self,
        target: Callable[..., None],
        args: tuple[Any, ...] = (),
        name: str = "",
        start: bool = False,
        daemon: bool = False,
    ) -> Thread:
        if not name:
            name = self.__class__.__name__

        self.log.i(f"create Thread: {target.__name__}, {name}", "create Thread")
        thread = Thread(
            target=target,
            args=args,
            name=name,
            daemon=daemon,
        )
        self.add_thread(thread)
        if start:
            thread.start()
        return thread

    def start_all_threads(self) -> None:
        for thread in self._threads:
            try:
                thread.start()
            except RuntimeError as exception:
                self.log.w(
                    f"Catch runtime exception on startup, still continuing: {exception}",
                    "start_all_threads",
                )

    def get_thread(self, name: str) -> Thread | None:
        for thread in self._threads:
            if thread.name == name:
                return thread
        return None

    def add_thread(self, thread: Thread) -> Thread:
        self._threads.append(thread)
        return thread

    def subscribe(self, subscriber: T) -> None:
        self.subscribers.append(subscriber)

    def shutdown_before_join(self) -> None:
        """
        Hook that gets executed before joining the threads and after the events
        have been set
        """

    def shutdown(self) -> None:
        self.log.i(f"Shutdown called for {self.__class__.__name__}", "shutdown")

        # hack, should be done in ShutdownAble who owns this event
        # but then we would need a different mechanism for saying finished, after we actually do so
        self.shutdown_event.set()

        self.shutdown_before_join()

        for thread in self._threads:
            if thread.is_alive():
                self.log.i(f"Shutdown {self.__class__.__name__}", "shutdown")
                #thread.join(timeout=5)
            else:
                self.log.i(
                    f"thread {self.__class__.__name__} is None or not alive", "shutdown"
                )

        self.log.i(f"Shutdown finished for {self.__class__.__name__}", "shutdown")
