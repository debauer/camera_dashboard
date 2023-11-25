from __future__ import annotations

from random import randrange

from dashboard.datatypes import Color

group_colors: dict[str, Color] = {}


def get_group_colors_dict() -> dict[str, Color]:
    return group_colors


def get_first_group_color(group_name: list[str]) -> Color:
    name = group_name[0]
    if name in group_colors:
        return group_colors[name]
    red = randrange(256)
    green = randrange(256)
    blue = randrange(256)
    group_colors[name] = Color(red, green, blue)
    return group_colors[name]


def get_lidar_color(lidar_name: str) -> Color:
    red = 0
    green = 255
    blue = int(lidar_name[1]) * 50
    if lidar_name[7] == "a":
        red = 255
    return Color(blue, green, red)
