import pygame
import random
import customtkinter

import config
import main_menu
import functions


def start_game(main_menu_window: customtkinter.CTk) -> None:
    """start_game close main menu and start the game

    Arguments:
        main_menu_window {customtkinter.CTk} -- tkinter main menu window
    """
    # -- loading settings
    dark_mode = True if main_menu_window["bg"] == "gray92" else False
    game_background_color = main_menu_window["bg"]

    # -- close main menu window
    main_menu_window.destroy()

    # -- pygame setup
    pygame.init()
    clock = pygame.time.Clock()
    is_running = True
    is_game_over = False
    font = pygame.font.SysFont("Helvetica", 20)

    # -- game components setup
    wall_color = "gray14" if dark_mode else "gray92"
    map_name = "map_1"
    walls, tanks = functions.map_reader(map_name)
    tank_a, tank_b = tanks
    tank_a["x"] = (tank_a["x"] * config.CELL_X) - config.CELL_X
    tank_a["x"] += config.CELL_X // 3
    tank_a["y"] = (tank_a["y"] * config.CELL_Y) - config.CELL_Y
    tank_a["y"] += config.CELL_Y // 3
    tank_b["x"] = (tank_b["x"] * config.CELL_X) - config.CELL_X
    tank_b["x"] += config.CELL_X // 3
    tank_b["y"] = (tank_b["y"] * config.CELL_Y) - config.CELL_Y
    tank_b["y"] += config.CELL_Y // 3
    tank_a = pygame.Rect(
        tank_a["x"], tank_a["y"], config.TANK_WIDTH, config.TANK_HEIGHT
    )
    tank_b = pygame.Rect(
        tank_b["x"], tank_b["y"], config.TANK_WIDTH, config.TANK_HEIGHT
    )
    tanks = [tank_a, tank_b]

    # -- game window size
    screen = pygame.display.set_mode(
        (config.GAME_SCREEN_WIDTH, config.GAME_SCREEN_HEIGHT)
    )

    # -- game loop
    while is_running:
        for event in pygame.event.get():
            # -- pygame.QUIT event means the user clicked X to close your window
            if event.type == pygame.QUIT:
                is_running = False
                # -- run main menu window again
                main_menu.start_main_menu()

        screen.fill(game_background_color)

        # -- get which key pressed by user (pygame.K_LEFT => left arrow and pygame.K_RIGHT => right arrow)
        tank_a, tank_b = tanks
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            pass
        # if keys[pygame.K_RIGHT]:
        #     spaceship_x += spaceship_speed
        if (
            keys[pygame.K_UP]
            and 10 <= tank_a.x
            and tank_a.x + config.TANK_WIDTH < config.GAME_SCREEN_WIDTH - 10
        ):
            tank_a.x += config.TANKS_SPEED
        if keys[pygame.K_DOWN] and 10 < tank_a.x < config.GAME_SCREEN_WIDTH - 10:
            tank_a.x -= config.TANKS_SPEED

        if (
            keys[pygame.K_w]
            and 10 <= tank_b.x
            and tank_b.x + config.TANK_WIDTH < config.GAME_SCREEN_WIDTH - 10
        ):
            tank_b.x += config.TANKS_SPEED
        if keys[pygame.K_s] and 10 < tank_b.x < config.GAME_SCREEN_WIDTH - 10:
            tank_b.x -= config.TANKS_SPEED

        tanks = functions.draw_map(
            screen=screen,
            wall_color=wall_color,
            walls=walls,
            background_color=game_background_color,
            font=font,
            tank_a=tank_a,
            tank_b=tank_b,
        )

        # -- update() the display to put your work on screen
        pygame.display.update()

        # -- limits FPS to 60
        clock.tick(60)

    pygame.quit()
