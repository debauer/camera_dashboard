from __future__ import annotations

from abc import abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class CollectAble(Generic[T]):
    """Abstract base class to show that the class provides something that can
    be collected.

    As it is designed as an abstract base class and not a mixin the {__init__}
    should actually be called. It sets up a basic subscriber array and maintains
    it with {self.subscribe}.
    """

    def __init__(self) -> None:
        self.subscribers: list[T] = []

    def subscribe(self, subscriber: T) -> None:
        """
        Subscriber mechanic where the subscriber gets notified of something that is collected.

        Generally recommended in some kind of {__init__} of the Subscriber so it should be:

            collectable.subscribe(self, scale=42)
        """
        self.subscribers.append(subscriber)


class NamedCollectAble(CollectAble[T], Generic[T]):
    """A {CollectAble} that also has a name.

    Similar to the main {CollectAble} this is also designed to call {__init__}.
    """

    def __init__(self) -> None:
        CollectAble.__init__(self)

    @abstractmethod
    def get_name(self) -> str:
        """Get the name of the specific thing you are collecting.

        One example where you could need this is the {VideoRecorder}. It uses
        {get_name} to determine how the file is named that will be the
        recording.

        Similarly the {NeuralNetwork} uses {get_name} to differentiate between
        cameras for their internal scheduling.
        """
