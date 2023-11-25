from __future__ import annotations

from datetime import datetime
from typing import List, NamedTuple, Tuple

from cv2 import Mat
from numpy import float64
from numpy.typing import NDArray

CameraName = str
Matrix = NDArray[float64]
Image = Mat
Size = Tuple[int, int]


class Point(NamedTuple):
    x: int
    y: int


class Points(NamedTuple):
    source: Point
    target: Point


Polygon = List[Point]
CollisionMap = List[List[int]]
HeatMapArray = NDArray[float64]


class LidarTransformation(NamedTuple):
    x: float
    y: float
    z: float
    angle: float


class LidarRawPoint(NamedTuple):
    distance: float
    angle: float
    row: int


LidarPoints = NDArray[float64]


class Box(NamedTuple):
    """
    A detection on a Frame, format::
        |-------|

        |[0]  [1]|

        |        |

        |[2]  [3]|

        |-------|
    """

    upper_right: Point
    upper_left: Point
    lower_left: Point
    lower_right: Point


class CalPoints(NamedTuple):
    source_points: list[Point]
    target_points: list[Point]


class Color(NamedTuple):
    blue: int
    green: int
    red: int


class Dimensions(NamedTuple):
    width: int
    height: int


class TaskTimestamp(NamedTuple):
    task: str
    time: datetime


Topic = str
