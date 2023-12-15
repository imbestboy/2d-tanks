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


def draw_map(
    screen: pygame.surface.Surface,
    wall_color: str,
    walls: list,
    background_color: str,
    font: pygame.font.SysFont,
    tank_a: dict,
    tank_b: dict,
) -> tuple:
    """draw_map draw game map on pygame screen

    Arguments:
        screen {pygame.surface.Surface} -- game screen to draw
        wall_color {str} -- color of walls in map
        walls {list} -- list of map's wall
        background_color {str} -- color of game background
        font {pygame.font.SysFont} -- font for type tank names
        tank_a {dict} -- horizontal and vertical tank a position
        tank_b {dict} -- horizontal and vertical tank b position

    Returns:
        tuple -- two list filled by pygame.Rect instances first list for walls and second for tanks
    """

    walls = [draw_wall(**wall, screen=screen, color=wall_color) for wall in walls]
    tanks = [
        draw_tank(
            **tank,
            screen=screen,
            tank_color=wall_color,
            background_color=background_color,
            font=font,
            tank_name=player,
        )
        for tank, player in zip((tank_a, tank_b), ("A", "B"))
    ]
    return walls, tanks


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


def draw_tank(
    screen: pygame.surface.Surface,
    x: int,
    y: int,
    tank_color: str,
    background_color: str,
    font: pygame.font.SysFont,
    tank_name: str,
) -> pygame.Rect:
    """draw_tank draw each tank in map

    Arguments:
        screen {pygame.surface.Surface} -- game screen
        x {int} -- tank horizontal location
        y {int} -- tank vertical location
        tank_color {str} -- color of tanks
        background_color {str} -- game background color
        font {pygame.font.SysFont} -- font for type tank names
        tank_name {str} -- name of tank ("A" or "B")

    Returns:
        pygame.Rect -- drawn tank
    """
    if 1 <= x <= 8:
        x = (x * config.CELL_X) - config.CELL_X
        x += config.CELL_X // 3
    if 1 <= y <= 8:
        y = (y * config.CELL_Y) - config.CELL_Y
        y += config.CELL_Y // 3
    tank_rect = pygame.Rect(x, y, config.TANK_WIDTH, config.TANK_HEIGHT)
    tank_pipe = pygame.Rect(
        tank_rect.centerx - 5,
        tank_rect.centery - (config.TANK_HEIGHT // 12) - 1,
        config.TANK_WIDTH // 2 + 5,
        config.TANK_HEIGHT // 6,
    )
    circle = pygame.draw.circle(
        screen,
        tank_color,
        (tank_rect.centerx - 5, tank_rect.centery - 1),
        tank_rect.height // 2 - 8,
        1,
    )
    pygame.draw.rect(screen, background_color, tank_pipe)
    pygame.draw.rect(screen, tank_color, tank_pipe, 1)
    circle = pygame.draw.circle(
        screen,
        background_color,
        (tank_rect.centerx - 5, tank_rect.centery - 1),
        tank_rect.height // 2 - 8 - 1,
    )
    pygame.draw.rect(screen, tank_color, tank_rect, 1)
    player_text = font.render(tank_name, True, tank_color)
    screen.blit(
        player_text,
        (
            circle.centerx - (player_text.get_width() // 2),
            circle.centery - (player_text.get_height() // 1.7),
        ),
    )

    return tank_rect
