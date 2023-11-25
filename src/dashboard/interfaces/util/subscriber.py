from __future__ import annotations

from abc import abstractmethod

from dashboard.datatypes import (
    EnrichedFrame,
    Image,
)


class ReaderSubscriber:
    @abstractmethod
    def push_image(self, frame: Image, stream_name: str) -> None:
        """
        A method where the frame from a CameraReader is pushed to a ReaderSubscriber.

        Important here is that this method should be as short as possible. We
        recommend a Producer-Consumer-like implementation, as the 'push' is
        happening on the main-Reader-thread.
        """


class EnrichedSubscriber:
    @abstractmethod
    def push_frame(self, frame: EnrichedFrame) -> None:
        """
        A method where the enriched frame from a FrameEnricher is pushed.

        Important here is that this method should be as short as possible. We
        recommend a Producer-Consumer-like implementation, as the 'push' is
        happening on the main-Enricher-thread.
        """

