import customtkinter
import json
import pygame

import config


def change_theme(theme: str) -> None:
    """change_theme change application theme

    Arguments:
        theme {str} -- only "dark" , "light" and "system"
    """
    if theme in ("dark", "light", "system"):
        customtkinter.set_appearance_mode(theme)
    else:
        raise ValueError("theme should be in 'dark' , 'light' and 'system'")


def draw_map(screen: pygame.surface.Surface, wall_color: str, map_name: str) -> None:
    """draw_map draw game map on pygame screen

    Arguments:
        screen {pygame.surface.Surface} -- game screen
        wall_color {str} -- color of walls in map
        map_name {str} -- name of map you want to draw
    """
    walls, tanks = map_reader(map_name)
    walls = [draw_wall(**wall, screen=screen, color=wall_color) for wall in walls]


def map_reader(name: str) -> tuple:
    """map_reader read and convert map json to python for draw

    Arguments:
        name {str} -- name of map you want to read

    Raises:
        ImportError: when map invalid

    Returns:
        tuple -- walls information and tanks respawn location
    """
    with open(f"maps/{name}.json", "r") as map_file:
        try:
            map_dict = json.loads(map_file.read())
            walls = map_dict["walls"]
            tanks = map_dict["tanks"]
        except:
            raise ImportError("map data not valid")

    return walls, tanks


def draw_wall(
    screen: pygame.surface.Surface, type: str, x: int, y: int, d: int, color: str
) -> pygame.Rect:
    """draw_wall draw each wall in pygame screen

    Arguments:
        screen {pygame.surface.Surface} -- game screen
        type {str} -- can be "h" for horizontal or "v" for vertical
        x {int} -- wall horizontal location
        y {int} -- wall vertical location
        d {int} -- length of wall
        color {str} -- color of wall

    Returns:
        pygame.Rect -- drawn wall
    """
    x *= config.CELL_X
    y *= config.CELL_Y
    if type == "h":
        y = y - config.WALL_THICKNESS if y == config.GAME_SCREEN_HEIGHT else y
        length = d * config.CELL_X
        wall = pygame.Rect(x, y, length, config.WALL_THICKNESS)
    else:
        x = x - config.WALL_THICKNESS if x == config.GAME_SCREEN_WIDTH else x
        length = d * config.CELL_Y
        wall = pygame.Rect(x, y, config.WALL_THICKNESS, length)
    pygame.draw.rect(screen, color, wall)
    return wall
