from __future__ import annotations

import numpy
from cv2 import (
    COLOR_BGR2GRAY,
    FONT_HERSHEY_SIMPLEX,
    LINE_8,
    THRESH_BINARY,
    addWeighted,
    bitwise_not,
    bitwise_or,
    circle,
    cvtColor,
    fillPoly,
    getTextSize,
    line,
    putText,
    threshold,
)
from numpy import array, zeros

from dashboard.datatypes import Box, Color, Image, Point, Polygon
from dashboard.datatypes.types import HeatMapArray


def remove_left(image: Image) -> Image:
    height = image.shape[0]
    width = image.shape[1]
    image[0:height, 0 : int(width / 2)] = Color(0, 0, 0)
    return image


def remove_right(image: Image) -> Image:
    height = image.shape[0]
    width = image.shape[1]
    image[0:height, int(width / 2) : width] = Color(0, 0, 0)
    return image


def split_image(dual_image: Image) -> tuple[Image, Image]:
    height = dual_image.shape[0]
    width = dual_image.shape[1]
    return (
        dual_image[0:height, 0 : int(width / 2)],
        dual_image[0:height, int(width / 2) : width],
    )


cached_masks: dict[str, Image] = {}


def mask_image(image: Image, mask: Image, cache_mask_id: str) -> Image:
    if cache_mask_id in cached_masks:
        mask = cached_masks[cache_mask_id]
    else:
        _th, mask = threshold(
            cvtColor(bitwise_not(mask), COLOR_BGR2GRAY), 253, 255, THRESH_BINARY
        )
        cached_masks[cache_mask_id] = bitwise_not(mask)

    return bitwise_or(image, image, mask=mask)


_WHITE = Color(255, 255, 255)
_BLACK = Color(0, 0, 0)


def draw_horizontal_line(
    image: Image, top: int, color: Color = _WHITE, line_width: int = 5
) -> Image:
    width = image.shape[1]
    return line(image, (0, top), (width, top), color, line_width)


def draw_vertical_line(
    image: Image, left: int, color: Color = _WHITE, line_width: int = 5
) -> Image:
    height = image.shape[0]
    return line(image, (left, 0), (left, height), color, line_width)


def draw_x(
    image: Image,
    left: int,
    top: int,
    color: Color = _BLACK,
    line_width: int = 2,
    size: int = 10,
) -> Image:
    left = max(left, 0)
    top = max(top, 0)
    image = line(
        image,
        (int(left - size / 2), top),
        (int(left + size / 2), top),
        color,
        line_width,
    )
    return line(
        image,
        (left, int(top - size / 2)),
        (left, int(top + size / 2)),
        color,
        line_width,
    )


def draw_points(
    image: Image,
    box: Box,
    color: Color = _BLACK,
    line_width: int = 2,
    size: int = 10,
) -> Image:
    for point in box:
        image = draw_x(image, int(point.x), int(point.y), color, line_width, size)
    return image


def draw_circle(
    image: Image,
    center: Point,
    radius: int = 100,
    color: Color = _BLACK,
    line_width: int = 2,
) -> Image:
    output: Image = circle(
        image, (int(center.x), int(center.y)), radius, color, line_width
    )
    return output


def draw_heat_map(image: Image, heat_map: HeatMapArray, color: Color) -> Image:
    blk = zeros(image.shape, numpy.float64)
    image_height, image_width = image.shape[:2]
    heat_map_height, heat_map_width = heat_map.shape[:2]
    y_size = int(image_height / heat_map_height)
    x_size = int(image_width / heat_map_width)
    for y_id, x_array in enumerate(heat_map):
        for x_id, value in enumerate(x_array):
            if value > 1:
                startx = int(x_size * x_id)
                starty = int(y_size * y_id)
                blk[starty : starty + y_size, startx : startx + x_size] = Color(
                    color.blue / 25 * value,
                    color.green / 25 * value,
                    color.red / 25 * value,
                )
    output: Image = addWeighted(image, 1.0, blk, 0.5, 1)
    return output


def draw_polygon_fill(
    image: Image, polygon: Polygon, color: Color = _BLACK, opacity: float = 0.50
) -> Image:
    blk = zeros(image.shape, numpy.float64)
    blk = fillPoly(blk, pts=[array(polygon)], color=color)
    output: Image = addWeighted(image, 1.0, blk, opacity, 1)
    return output


def draw_polygon(
    image: Image,
    polygon: Polygon,
    color: Color = _BLACK,
    line_width: int = 1,
    fill: bool = False,
    fill_opacity: float = 0.50,
) -> Image:
    for index in range(0, len(polygon)):
        next_index = (index + 1) % len(polygon)
        image = line(image, polygon[index], polygon[next_index], color, line_width)
    if fill:
        image = draw_polygon_fill(image, polygon, color, fill_opacity)
    return image


def draw_detection_box(
    image: Image,
    box: Box,
    color: Color = _BLACK,
    line_width: int = 2,
) -> Image:
    image = line(image, box.upper_left, box.upper_right, color, line_width)
    image = line(image, box.upper_right, box.lower_right, color, line_width)
    image = line(image, box.lower_right, box.lower_left, color, line_width)
    return line(image, box.lower_left, box.upper_left, color, line_width)


_DEFAULT_TEXT_POSITION = Point(15, 65)


def add_text_to_image(
    image: Image,
    text: str,
    position: Point = _DEFAULT_TEXT_POSITION,
    font: int = FONT_HERSHEY_SIMPLEX,
    font_scale: float = 2.0,
    color: Color = _WHITE,
    thickness: int = 4,
    line_type: int = LINE_8,
    copy: bool = True,
) -> Image:
    img: Image = numpy.copy(image) if copy else image

    text_size = getTextSize("test", font, font_scale, thickness)
    line_height = text_size[1] + 50

    position_x, position_y = position
    for i, text_line in enumerate(text.split("\n")):
        line_adjusted_y = position_y + i * line_height
        putText(
            img,
            text_line,
            (position_x, line_adjusted_y),
            font,
            font_scale,
            color,
            thickness,
            line_type,
        )

    return img
