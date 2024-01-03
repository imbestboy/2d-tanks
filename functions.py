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


def map_reader(name: str) -> tuple:
    """map_reader read and convert map json to python for draw

    Arguments:
        name {str} -- name of map you want to read

    Raises:
        ImportError: when map invalid

    Returns:
        tuple -- walls information and tanks spawn location and tanks respawn location
    """
    with open(f"maps/{name}.json", "r") as map_file:
        try:
            map_dict = json.loads(map_file.read())
            walls = map_dict["walls"]
            tanks = map_dict["tanks"]
            respawn = map_dict["respawn"]
        except:
            raise ImportError("map data not valid")

    return (walls, tanks, respawn)


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


def blit_rotate_center(
    screen: pygame.surface.Surface,
    image: pygame.surface.Surface,
    top_left: tuple,
    angle: int,
):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    screen.blit(rotated_image, new_rect.topleft)
    return new_rect


def show_winner_score(
    winner_score: float, winner_score_label: customtkinter.CTkLabel
) -> None:
    """show_winner_score show winner score label next to winner score slider for end user with every slider move

    Arguments:
        speed_value {float} -- spaceship speed
        spaceship_speed_label {customtkinter.CTkLabel} -- label to show spaceship speed
    """
    winner_score = int(winner_score)
    winner_score_label.configure(text=winner_score)


def convert_location_to_pixel(x: int, y: int) -> tuple:
    """convert_location_to_pixel get x and y in cell and convert to pixel for show to user

    Arguments:
        x {int} -- cell x
        y {int} -- cell y

    Returns:
        tuple -- x pixel and y pixel
    """
    x = (x * config.CELL_X) - config.CELL_X
    x += config.CELL_X // 3
    y = (y * config.CELL_Y) - config.CELL_Y
    y += config.CELL_Y // 3
    return x, y
